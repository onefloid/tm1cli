from TM1py import Process


class MockedViewService:

    def get_all_names(self, cube_name: str):
        return ["View1", "View2", "View3"]

    def exists(self, cube_name: str, view_name: str, private: bool):
        if "not" in view_name.lower():
            return False
        else:
            return True


class MockedProcessService:
    def exists(self, process_name: str):
        return False if "not" in process_name else True

    def get(self, process_name: str):
        return Process(process_name)

    def update_or_create(self, process: Process):
        return f"Process {process.name} was tested mocked."


class MockedTM1Service:
    def __init__(self, **kwargs) -> None:
        self.views = MockedViewService()
        self.processes = MockedProcessService()

    def __enter__(self):
        """
        Context manager entry point.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Context manager exit point. Clean up resources if needed.
        """
        pass
