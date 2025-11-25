
from data_pipeline.run_pipeline import main

def test_pipeline_runs_successfully():
    # Le test doit passer si le pipeline ne crash pas
    main()
