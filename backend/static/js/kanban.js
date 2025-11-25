document.addEventListener("DOMContentLoaded", function () {
    console.log("kanban.js cargado");

    let draggedCard = null;

    // === Obtener CSRF desde cookies (Django) ===
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie("csrftoken");

    // =====================================================================================
    //                               DRAG & DROP
    // =====================================================================================
    function initDragAndDrop() {
        const taskCards = document.querySelectorAll(".task-card");
        const columns = document.querySelectorAll(".droppable-column");

        console.log("Encontradas tarjetas:", taskCards.length);
        console.log("Encontradas columnas:", columns.length);

        // ---------- Eventos de arrastre ----------
        taskCards.forEach(card => {
            card.addEventListener("dragstart", function (e) {
                console.log("dragstart:", card.dataset.taskId);

                draggedCard = card;
                e.dataTransfer.effectAllowed = "move";

                // Imagen sólida para arrastrar
                const dragImage = card.cloneNode(true);
                dragImage.style.position = "absolute";
                dragImage.style.top = "-9999px";
                dragImage.style.left = "-9999px";
                dragImage.style.boxShadow = "0px 4px 10px rgba(0,0,0,0.3)";
                dragImage.style.opacity = "1";
                document.body.appendChild(dragImage);

                e.dataTransfer.setDragImage(dragImage, 0, 0);

                setTimeout(() => document.body.removeChild(dragImage), 0);
            });

            card.addEventListener("dragend", function () {
                console.log("dragend");
                draggedCard = null;
            });
        });

        // ---------- Eventos de drop ----------
        columns.forEach(col => {
            col.addEventListener("dragover", function (e) {
                e.preventDefault();
            });

            col.addEventListener("drop", function (e) {
                e.preventDefault();
                if (!draggedCard) return;

                const taskId = draggedCard.dataset.taskId;
                const columnId = col.dataset.columnId;

                console.log(`Drop tarea ${taskId} en columna ${columnId}`);

                // Mover visualmente
                col.appendChild(draggedCard);

                // Obtener orden actualizado de tareas
                const orderedTaskIds = Array.from(
                    col.querySelectorAll(".task-card")
                ).map(card => card.dataset.taskId);

                console.log("Nuevo orden:", orderedTaskIds);

                // Enviar al backend
                fetch("/tasks/mover/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrftoken,
                    },
                    body: JSON.stringify({
                        task_id: taskId,
                        column_id: columnId,
                        ordered_task_ids: orderedTaskIds,
                    }),
                })
                    .then(res => res.json().catch(() => null))
                    .then(data => console.log("Respuesta backend:", data))
                    .catch(err => console.error("Error fetch:", err));
            });
        });
    }

    // =====================================================================================
    //                               FILTROS
    // =====================================================================================
    function initFilters() {
        const priorityFilter = document.getElementById("priority-filter");
        const tagFilter = document.getElementById("tag-filter");
        const dueFilter = document.getElementById("due-filter");
        const tasks = document.querySelectorAll(".task-card");

        // ---------- Construir opciones de etiquetas ----------
        if (tagFilter) {
            const tagSet = new Set();

            tasks.forEach(task => {
                const tagsStr = task.dataset.tags || "";
                tagsStr.split(",")
                    .map(t => t.trim())
                    .filter(t => t)
                    .forEach(t => tagSet.add(t));
            });

            tagSet.forEach(tagName => {
                const opt = document.createElement("option");
                opt.value = tagName;
                opt.textContent = tagName;
                tagFilter.appendChild(opt);
            });
        }

        // ---------- Función principal de filtrado ----------
        function applyFilters() {
            const selectedPriority = priorityFilter ? priorityFilter.value : "";
            const selectedTag = tagFilter ? tagFilter.value : "";
            const selectedDue = dueFilter ? dueFilter.value : "";

            const today = new Date();
            today.setHours(0, 0, 0, 0);

            tasks.forEach(task => {
                const taskPriority = task.dataset.priority;
                const taskTags = (task.dataset.tags || "")
                    .split(",")
                    .map(t => t.trim())
                    .filter(t => t);

                const dueStr = task.dataset.due || "";
                let matchPriority = true;
                let matchTag = true;
                let matchDue = true;

                // ----- PRIORIDAD -----
                if (selectedPriority !== "") {
                    matchPriority = (taskPriority === selectedPriority);
                }

                // ----- ETIQUETA -----
                if (selectedTag !== "") {
                    matchTag = taskTags.includes(selectedTag);
                }

                // ----- FECHA -----
                if (selectedDue !== "") {
                    if (dueStr === "") {
                        matchDue = (selectedDue === "none");
                    } else {
                        const taskDate = new Date(dueStr);
                        taskDate.setHours(0, 0, 0, 0);

                        if (selectedDue === "overdue") {
                            matchDue = (taskDate < today);
                        } else if (selectedDue === "today") {
                            matchDue = (taskDate.getTime() === today.getTime());
                        } else if (selectedDue === "future") {
                            matchDue = (taskDate > today);
                        }
                    }
                }

                // ----- Aplicar los 3 filtros -----
                if (matchPriority && matchTag && matchDue) {
                    task.style.display = "";
                } else {
                    task.style.display = "none";
                }
            });
        }

        // Eventos de cambio en filtros
        if (priorityFilter) priorityFilter.addEventListener("change", applyFilters);
        if (tagFilter) tagFilter.addEventListener("change", applyFilters);
        if (dueFilter) dueFilter.addEventListener("change", applyFilters);
    }

    // Iniciar todo
    initDragAndDrop();
    initFilters();
});
