from TM1py import Process


class MockedCubeService:
    cubes = ["Cube1", "Cube2"]

    def get_all_names(self, cube_name: str):
        return self.cubes

    def exists(self, cube_name: str):
        return cube_name in self.cubes


class MockedViewService:

    def get_all_names(self, cube_name: str):
        return ["View1", "View2", "View3"]

    def exists(self, cube_name: str, view_name: str, private: bool):
        if "not" in view_name.lower():
            return False
        else:
            return True


class MockedDimensionService:
    def get_all_names(self, skip_control_dims: bool):
        return ["Dimension1", "Dimension2", "Dimension3"]

    def exists(self, dimension_name: str):
        if "not" in dimension_name.lower():
            return False
        else:
            return True


class MockedSubsetService:
    def get_all_names(self, dimension_name: str):
        return ["Subset1", "Subset2", "Subset3"]

    def exists(self, dimension_name: str, subset_name: str, private: bool):
        if "not" in subset_name.lower():
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
        self.cubes = MockedCubeService()
        self.dimensions = MockedDimensionService()
        self.subsets = MockedSubsetService()

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
