import pendulum

from airflow.models.dag import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

with DAG(
    dag_id="flight_data_etl_dag",
    start_date=pendulum.datetime(2025, 6, 2, tz="America/Los_Angeles"), # Adjust to your desired start date
    catchup=False,
    schedule="@daily",
    tags=["etl", "application", "kubernetes"],
    doc_md="""\
    ### ETL Application DAG using KubernetesPodOperator
    """,
) as dag:
    k8s_namespace = "airflow"

    extract_task = KubernetesPodOperator(
        task_id="extract_flight_data",
        namespace=k8s_namespace,
        image="taekunkim/flight-delays-etl:dev",
        cmds=["python"],
        arguments=["/usr/src/app/src/etl/extract/flight_data.py"],
        name="etl-extract-pod", 
        is_delete_operator_pod=True, 
        get_logs=True, 
        # env_vars={'EXTRACT_DATE': '{{ ds }}'},
        doc_md="""\
        #### Extract Task (KubernetesPodOperator)
        """,
    )

    # # 2. Transform Task
    # # This task runs your transformation script inside a specified Docker image.
    # # Replace 'your-repo/your-transform-image:latest' with your actual image.
    # # Replace ['python', '/app/transform_script.py'] with your actual command and arguments.
    # transform_task = KubernetesPodOperator(
    #     task_id="transform_data_k8s",
    #     namespace=k8s_namespace,
    #     image="your-repo/your-transform-image:latest",  # REPLACE with your transform image
    #     cmds=["python"],
    #     arguments=["/app/transform_script.py"], # Example: "--input-path", "/data/extracted_data.csv"
    #                                             # You might need to use XComs or shared volumes to pass data
    #     name="etl-transform-pod",
    #     is_delete_operator_pod=True,
    #     get_logs=True,
    #     doc_md="""\
    #     #### Transform Task (KubernetesPodOperator)
    #     Runs the data transformation process in a dedicated Kubernetes pod.
    #     Replace `image`, `cmds`, and `arguments` with your specific transformation logic.
    #     Consider how data from the extract step will be made available (e.g., shared PVC, XComs for small data).
    #     """,
    # )

    # # 3. Load Task
    # # This task runs your loading script inside a specified Docker image.
    # # Replace 'your-repo/your-load-image:latest' with your actual image.
    # # Replace ['python', '/app/load_script.py'] with your actual command and arguments.
    # load_task = KubernetesPodOperator(
    #     task_id="load_data_k8s",
    #     namespace=k8s_namespace,
    #     image="your-repo/your-load-image:latest",  # REPLACE with your load image
    #     cmds=["python"],
    #     arguments=["/app/load_script.py"], # Example: "--input-path", "/data/transformed_data.csv"
    #     name="etl-load-pod",
    #     is_delete_operator_pod=True,
    #     get_logs=True,
    #     doc_md="""\
    #     #### Load Task (KubernetesPodOperator)
    #     Runs the data loading process in a dedicated Kubernetes pod.
    #     Replace `image`, `cmds`, and `arguments` with your specific loading logic.
    #     Consider how data from the transform step will be made available.
    #     """,
    # )

    # Define the task dependencies (sequence)
    # Extract -> Transform -> Load
    extract_task # >> transform_task >> load_task
