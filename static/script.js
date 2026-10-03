async function loadTasks() {
    const res = await fetch("/api/tasks");
    const tasks = await res.json();
    const list = document.getElementById("taskList");
    list.innerHTML = "";

    tasks.forEach(task => {
        const li = document.createElement("li");
        if (task.done) li.classList.add("done");

        const span = document.createElement("span");
        span.textContent = task.title;
        span.onclick = () => toggleTask(task.id);

        const btn = document.createElement("button");
        btn.textContent = "Delete";
        btn.onclick = () => deleteTask(task.id);

        li.appendChild(span);
        li.appendChild(btn);
        list.appendChild(li);
    });
}

async function addTask() {
    const input = document.getElementById("taskInput");
    if (!input.value.trim()) return;

    await fetch("/api/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: input.value })
    });
    input.value = "";
    loadTasks();
}

async function toggleTask(id) {
    await fetch(`/api/tasks/${id}`, { method: "PUT" });
    loadTasks();
}

async function deleteTask(id) {
    await fetch(`/api/tasks/${id}`, { method: "DELETE" });
    loadTasks();
}

loadTasks();
