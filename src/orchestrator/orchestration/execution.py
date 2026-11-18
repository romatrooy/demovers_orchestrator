class ExecutionManager:
    async def process_executable_tasks(self, graph_id: str) -> None: ...

    async def run_single_task(self, task: Task) -> None:
        # 1. (если повтор) base_freshness_check → submit_report
        # 2. assign
        # 3. get_execution_package
        # 4. start_attempt
        # 5. запуск агента
        # 6. complete/fail
        # 7. scope_check → submit_report
        ...
