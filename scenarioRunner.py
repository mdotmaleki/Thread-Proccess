# scenario_runner.py

from process_manager import ProcessManager
from thread_manager import ThreadManager


thread_manager = ThreadManager()

process_manager = ProcessManager()


SCENARIO_MAP = {
    "thread": {
        "define": {
            "define_1": thread_manager.thread_define_1,
            "define_2": thread_manager.thread_define_2,
            "define_3": thread_manager.thread_define_3,
        },
        "current": {
            "current_1": thread_manager.thread_current_1,
            "current_2": thread_manager.thread_current_2,
            "current_3": thread_manager.thread_current_3,
        },
        "subclass": {
            "subclass_1": thread_manager.thread_subclass_1,
            "subclass_2": thread_manager.thread_subclass_2,
            "subclass_3": thread_manager.thread_subclass_3,
        },
        "lock": {
            "lock_1": thread_manager.thread_lock_1,
            "lock_2": thread_manager.thread_lock_2,
            "lock_3": thread_manager.thread_lock_3,
        },
        "rlock": {
            "rlock_1": thread_manager.thread_rlock_1,
            "rlock_2": thread_manager.thread_rlock_2,
            "rlock_3": thread_manager.thread_rlock_3,
        },
        "semaphore":{
            "semaphore_1": thread_manager.thread_semaphore_1,
            "semaphore_2": thread_manager.thread_semaphore_2,
            "semaphore_3": thread_manager.thread_semaphore_3,
        },
        "condition":{
            "condition_1": thread_manager.thread_condition_1,
            "condition_2": thread_manager.thread_condition_2,
            "condition_3": thread_manager.thread_condition_3,
        },
        "event":{
            "event_1": thread_manager.thread_event_1,
            "event_2": thread_manager.thread_event_2,
            "event_3": thread_manager.thread_event_3,
        },
        "barrier":{
            "barrier_1": thread_manager.thread_barrier_1,
            "barrier_2": thread_manager.thread_barrier_2,
            "barrier_3": thread_manager.thread_barrier_3,
        },
        "queue":{
            "queue_1": thread_manager.thread_queue_1,
            "queue_2": thread_manager.thread_queue_2,
            "queue_3": thread_manager.thread_queue_3,
        }

    },

    "process": {
        "spawning": {
            "spawn_1": process_manager.spawn_scenario_1,
            "spawn_2": process_manager.spawn_scenario_2,
            "spawn_3": process_manager.spawn_scenario_3,
        },
        "naming": {
            "naming_1": process_manager.naming_scenario_1,
            "naming_2": process_manager.naming_scenario_2,
            "naming_3": process_manager.naming_scenario_3,
        },
        "background": {
            "background_1": process_manager.background_scenario_1,
            "background_2": process_manager.background_scenario_2,
            "background_3": process_manager.background_scenario_3,
        },
        "killing": {
            "killing_1": process_manager.killing_scenario_1,
            "killing_2": process_manager.killing_scenario_2,
            "killing_3": process_manager.killing_scenario_3,
        },
        "subclass": {
            "subclass_1": process_manager.subclass_scenario_1,
            "subclass_2": process_manager.subclass_scenario_2,
            "subclass_3": process_manager.subclass_scenario_3,
        },
        "queue": {
            "queue_1": process_manager.queue_scenario_1,
            "queue_2": process_manager.queue_scenario_2,
            "queue_3": process_manager.queue_scenario_3,
        },
        "pipe":{
            "pipe_1": process_manager.pipe_scenario_1,
            "pipe_2": process_manager.pipe_scenario_2,
            "pipe_3": process_manager.pipe_scenario_3,
        },
        "barrier":{
            "barrier_1": process_manager.barrier_scenario_1,
            "barrier_2": process_manager.barrier_scenario_2,
            "barrier_3": process_manager.barrier_scenario_3,
        },
        "pool":{
            "pool_1": process_manager.pool_scenario_1,
            "pool_2": process_manager.pool_scenario_2,
            "pool_3": process_manager.pool_scenario_3,
        },

    }
}


def run_scenario(method: str, tool: str, scenario: int):
    try:
        func = SCENARIO_MAP[method][tool][scenario]
    except KeyError:
        return None  # یعنی چنین سناریویی وجود ندارد

    return func()