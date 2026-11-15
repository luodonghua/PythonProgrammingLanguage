"""Assignment 5: context isolation between asyncio tasks.

``request_id`` is a ContextVar with default ``"-"`` (given below).

``handle(rid, steps)`` is a coroutine. It sets ``request_id`` to ``rid``, then
awaits ``asyncio.sleep(0)`` ``steps`` times (letting other tasks run). After
each sleep it records ``request_id.get()``. It returns the list of recorded
values (length ``steps``). Because every task has its own context, each task
must see only its own ``rid``.

``handle_all(ids, steps=3)`` is a coroutine. It runs ``handle(rid, steps)`` for
every id *concurrently* with ``asyncio.gather`` and returns the list of results
in the same order as ``ids``. The ``request_id`` of the caller must stay
unchanged (still ``"-"``) afterwards.

``child_inherits(rid)`` is a coroutine. It sets ``request_id`` to ``rid``, then
creates a task (``asyncio.create_task``) running an inner coroutine that
(1) reads ``request_id`` and (2) sets it to ``"changed-by-child"``. Await the
task. Return the tuple ``(value_child_saw_first, value_parent_sees_after)``.
A task copies the context when it is created, so the child sees ``rid`` and the
parent still sees ``rid`` afterwards.
"""

import asyncio
import contextvars

request_id = contextvars.ContextVar("request_id", default="-")


async def handle(rid, steps):
    """Set the id, yield to other tasks ``steps`` times, record the id each time."""
    request_id.set(rid)
    seen = []
    for _ in range(steps):
        await asyncio.sleep(0)
        seen.append(request_id.get())
    return seen


async def handle_all(ids, steps=3):
    """Run ``handle`` for all ids concurrently; return results in order."""
    return list(await asyncio.gather(*(handle(rid, steps) for rid in ids)))


async def child_inherits(rid):
    """Show that a child task starts with a copy of the parent's context."""
    request_id.set(rid)

    async def child():
        first = request_id.get()
        request_id.set("changed-by-child")
        return first

    seen_by_child = await asyncio.create_task(child())
    return seen_by_child, request_id.get()


if __name__ == "__main__":
    print(asyncio.run(handle_all(["a", "b"], 2)))
