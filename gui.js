let currentUser = null;
let booksList = [];
let usersList = [];
let historyList = [];

// Wait for webview API to be loaded
window.addEventListener('pywebviewready', function() {
    // Automatically initialize dashboard data or check session
    showToast("Sistema de Biblioteca Conectado exitosamente.", "success");
});

// Toast notifications
function showToast(message, type = "success") {
    const toast = document.getElementById("toast");
    const icon = document.getElementById("toast-icon");
    const msg = document.getElementById("toast-message");
    
    msg.textContent = message;
    toast.className = `toast ${type}`;
    
    if (type === "success") {
        icon.innerHTML = `<svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>`;
    } else {
        icon.innerHTML = `<svg viewBox="0 0 24 24"><path d="M12 2C6.47 2 2 6.47 2 12s4.47 10 10 10 10-4.47 10-10S17.53 2 12 2zm5 13.59L15.59 17 12 13.41 8.41 17 7 15.59 10.59 12 7 8.41 8.41 7 12 10.59 15.59 7 17 8.41 13.41 12 17 15.59z"/></svg>`;
    }
    
    toast.style.display = "flex";
    setTimeout(() => {
        toast.style.display = "none";
    }, 4000);
}

// Login Tabs Switching
function setLoginMode(isLogin) {
    document.getElementById("tab-login").className = isLogin ? "login-tab active" : "login-tab";
    document.getElementById("tab-register").className = !isLogin ? "login-tab active" : "login-tab";
    document.getElementById("login-form").style.display = isLogin ? "flex" : "none";
    document.getElementById("register-form").style.display = !isLogin ? "flex" : "none";
}

// Handle Login
function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById("login-email").value;
    const pass = document.getElementById("login-pass").value;

    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.login(email, pass).then(response => {
            if (response.success) {
                currentUser = response.usuario;
                showToast(`Bienvenido/a, ${currentUser.nombre}!`, "success");
                document.getElementById("login-container").style.display = "none";
                
                // Setup Navbar/Profile
                document.getElementById("nav-user-name").textContent = currentUser.nombre;
                document.getElementById("nav-user-role").textContent = currentUser.role;
                document.getElementById("avatar").textContent = currentUser.nombre.substring(0, 2).toUpperCase();

                // Hide admin options if Client
                const adminElements = document.querySelectorAll(".role-admin-only");
                adminElements.forEach(elem => {
                    if (currentUser.role !== "Bibliotecario") {
                        elem.style.setProperty('display', 'none', 'important');
                    } else {
                        elem.style.display = "";
                    }
                });

                // Hide client options if Admin
                const clientElements = document.querySelectorAll(".role-client-only");
                clientElements.forEach(elem => {
                    if (currentUser.role !== "Cliente") {
                        elem.style.setProperty('display', 'none', 'important');
                    } else {
                        elem.style.display = "";
                    }
                });

                // Default Navigation
                switchView('dash');
                refreshData();
            } else {
                showToast(response.message, "error");
            }
        }).catch(err => {
            showToast("Error de conexión al servidor local.", "error");
        });
    } else {
        // Mock for testing in regular browsers
        currentUser = { nombre: "Administrador Demo", role: "Bibliotecario", idUsuario: "L01" };
        document.getElementById("login-container").style.display = "none";
        switchView('dash');
        showToast("Ejecutando en modo de demostración del navegador.", "success");
    }
}

// Handle Register
function handleRegister(e) {
    e.preventDefault();
    const id = document.getElementById("reg-id").value;
    const nombre = document.getElementById("reg-nombre").value;
    const email = document.getElementById("reg-email").value;
    const pass = document.getElementById("reg-pass").value;

    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.registrar_usuario(id, nombre, email, pass, "Cliente").then(response => {
            if (response.success) {
                showToast(response.message, "success");
                // Clear inputs
                document.getElementById("reg-id").value = "";
                document.getElementById("reg-nombre").value = "";
                document.getElementById("reg-email").value = "";
                document.getElementById("reg-pass").value = "";
                // Switch back to login
                setLoginMode(true);
                document.getElementById("login-email").value = email;
            } else {
                showToast(response.message, "error");
            }
        });
    }
}

function handleLogout() {
    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.logout().then(res => {
            currentUser = null;
            document.getElementById("login-container").style.display = "flex";
        });
    } else {
        currentUser = null;
        document.getElementById("login-container").style.display = "flex";
    }
}

// Navigation
function switchView(viewId) {
    // Update Active Menu
    const menuItems = document.querySelectorAll(".menu-item");
    menuItems.forEach(item => item.classList.remove("active"));
    
    // Assign active to clicked
    let activeMenu = document.getElementById(`menu-${viewId}`);
    if (activeMenu) activeMenu.classList.add("active");
    
    // Hide all views
    const views = document.querySelectorAll(".view-section");
    views.forEach(view => view.classList.remove("active"));
    
    // Show requested view
    const targetView = document.getElementById(`view-${viewId}`);
    if (targetView) targetView.classList.add("active");

    // Update title
    const titleMap = {
        'dash': ['Dashboard', 'Resumen ejecutivo y operaciones rápidas del sistema'],
        'catalog': ['Catálogo de Libros', 'Inventario completo de libros de la biblioteca'],
        'loans': ['Mis Préstamos', 'Seguimiento de libros prestados y fechas de vencimiento'],
        'users': ['Usuarios Registrados', 'Listado dinámico de usuarios en el sistema'],
        'visualizer': ['Catálogo Visual', 'Representación gráfica e interactiva del catálogo de libros'],
        'loan-history': ['Historial de Préstamos', 'Registro completo de salidas y devoluciones de libros']
    };

    document.getElementById("view-title").textContent = titleMap[viewId][0];
    document.getElementById("view-subtitle").textContent = titleMap[viewId][1];

    // Refresh specific visualizer content or table data
    if (viewId === 'visualizer') {
        renderStructureGraphic('bst');
    } else if (viewId === 'loan-history') {
        loadLoanHistory();
    } else {
        refreshData();
    }
}

// Global Data Refresher
function refreshData() {
    if (!window.pywebview || !window.pywebview.api) return;

    // 1. Get catalogue
    window.pywebview.api.obtener_catalogo_ordenado().then(books => {
        booksList = books;
        document.getElementById("stat-books-count").textContent = books.length;
        renderCatalog(books);
    });

    // 2. Get users
    window.pywebview.api.obtener_todos_usuarios().then(users => {
        usersList = users;
        document.getElementById("stat-users-count").textContent = users.length;
        renderUsersTable(users);
        
        // Active loans calculation from users
        let activeLoans = 0;
        users.forEach(u => {
            activeLoans += u.prestamosActivosCount;
        });
        document.getElementById("stat-loans-count").textContent = activeLoans;
    });

    // 3. Get recent history (Stack)
    window.pywebview.api.obtener_historial_operaciones(15).then(history => {
        historyList = history;
        document.getElementById("stat-history-count").textContent = history.length;
        renderTimeline(history);
    });

    // 4. Get active loans if Client
    if (currentUser && currentUser.role === "Cliente") {
        window.pywebview.api.obtener_prestamos_cliente(currentUser.idUsuario).then(loans => {
            renderLoansTable(loans);
        });
    }
}

// Render Books Catalog
function renderCatalog(books) {
    const grid = document.getElementById("catalog-grid");
    grid.innerHTML = "";

    if (books.length === 0) {
        grid.innerHTML = `
            <div class="glass-panel" style="grid-column: 1/-1; padding: 40px; text-align: center; color: var(--text-secondary);">
                No hay libros en el catálogo de la biblioteca.
            </div>
        `;
        return;
    }

    books.forEach(libro => {
        const card = document.createElement("div");
        card.className = `book-card glass-panel ${libro.estado}`;
        
        const isAvailable = libro.estado === "Disponible";
        
        // Build footer buttons based on role and availability
        let footerHtml = '';
        if (currentUser.role === "Bibliotecario") {
            footerHtml = `
                <button class="btn btn-secondary btn-danger" style="flex:1; padding: 6px 12px; font-size:0.8rem;" onclick="handleDeleteBook('${libro.isbn}')">Eliminar</button>
                <button class="btn" style="flex:1.5; padding: 6px 12px; font-size:0.8rem;" onclick="showLoanReturnModal('${libro.isbn}', '${libro.titulo}', ${isAvailable})">
                    ${isAvailable ? 'Prestar' : 'Devolución'}
                </button>
            `;
        } else {
            // Client controls
            if (isAvailable) {
                footerHtml = `
                    <button class="btn btn-success" style="width:100%; padding: 8px;" onclick="handleClientRequestLoan('${libro.isbn}')">Solicitar Préstamo</button>
                `;
            } else {
                footerHtml = `
                    <button class="btn btn-secondary" style="width:100%; padding: 8px;" onclick="handleClientRequestLoan('${libro.isbn}')">
                        Unirse a Lista de Espera
                    </button>
                `;
            }
        }

        card.innerHTML = `
            <div class="book-header">
                <span class="book-isbn">${libro.isbn}</span>
                <span class="book-badge ${libro.estado}">${libro.estado}</span>
            </div>
            <div style="display:flex; flex-direction:column; gap:4px;">
                <h4 class="book-title" title="${libro.titulo}">${libro.titulo}</h4>
                <span class="book-autor">por ${libro.autor}</span>
            </div>
            <div id="queue-indicator-${libro.isbn}" style="font-size:0.75rem; color:var(--accent-amber); display:none;">
                <!-- Waitlist info -->
            </div>
            <div class="book-footer">
                ${footerHtml}
            </div>
        `;
        grid.appendChild(card);

        // Fetch waiting queue count
        if (window.pywebview && window.pywebview.api) {
            window.pywebview.api.obtener_cola_de_espera(libro.isbn).then(cola => {
                if (cola && cola.length > 0) {
                    const indicator = document.getElementById(`queue-indicator-${libro.isbn}`);
                    if (indicator) {
                        indicator.style.display = "block";
                        indicator.textContent = `⚠️ En espera: ${cola.length} persona(s)`;
                    }
                }
            });
        }
    });
}

// Handle Search Instant typing
function handleSearchBooks() {
    const query = document.getElementById("catalog-search-input").value;
    const criterio = document.getElementById("catalog-search-criterio").value;

    if (!query.trim()) {
        refreshData();
        return;
    }

    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.buscar_libro(criterio, query).then(results => {
            renderCatalog(results);
        });
    }
}

// Render Users Table
function renderUsersTable(users) {
    const tbody = document.getElementById("users-table-body");
    tbody.innerHTML = "";

    if (users.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; color:var(--text-secondary);">No hay usuarios registrados.</td></tr>`;
        return;
    }

    users.forEach(u => {
        const tr = document.createElement("tr");
        const showDelete = currentUser.role === "Bibliotecario" && u.idUsuario !== currentUser.idUsuario;
        const deleteButton = showDelete ? `<button class="btn btn-secondary btn-danger" style="padding:6px 12px; font-size:0.75rem;" onclick="handleDeleteUser('${u.idUsuario}', '${u.nombre}')">Eliminar</button>` : `<span style="color:var(--text-muted);">Sin acciones</span>`;
        
        tr.innerHTML = `
            <td><strong>${u.idUsuario}</strong></td>
            <td>${u.nombre}</td>
            <td>${u.correo}</td>
            <td><span class="book-badge" style="background:${u.role==='Bibliotecario'?'rgba(168,85,247,0.15)':'rgba(59,130,246,0.15)'}; color:${u.role==='Bibliotecario'?'var(--accent-purple)':'var(--accent-blue)'}; border:none;">${u.role}</span></td>
            <td>${u.codigoEmpleado || '-'}</td>
            <td>${u.prestamosActivosCount || '0'}</td>
            <td class="role-admin-only">${deleteButton}</td>
        `;
        tbody.appendChild(tr);
    });
}

// Render Loans Table for clients
function renderLoansTable(loans) {
    const tbody = document.getElementById("loans-table-body");
    tbody.innerHTML = "";

    if (loans.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; color:var(--text-secondary);">No tienes préstamos activos actualmente.</td></tr>`;
        return;
    }

    loans.forEach(l => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><strong>${l.titulo}</strong><br><small style="color:var(--text-secondary);">por ${l.autor}</small></td>
            <td style="color:var(--accent-purple); font-weight:600;">${l.isbn}</td>
            <td>${l.fecha_salida}</td>
            <td>${l.fecha_limite}</td>
            <td><span class="book-badge Prestado">Activo</span></td>
            <td>
                <button class="btn btn-success" style="padding: 6px 12px; font-size:0.8rem;" onclick="handleClientReturnBook('${l.isbn}')">
                    Devolver Libro
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// Render History timeline
function renderTimeline(history) {
    const container = document.getElementById("dash-timeline");
    container.innerHTML = "";

    if (history.length === 0) {
        container.innerHTML = `<div style="text-align:center; color:var(--text-muted); padding: 20px;">No hay historial registrado.</div>`;
        return;
    }

    history.forEach((desc, idx) => {
        const item = document.createElement("div");
        item.className = "stack-item";
        
        // Highlight the top element of the stack
        if (idx === 0) {
            item.innerHTML = `
                <span class="stack-badge">TOPE (Pop)</span>
                <p style="padding-right: 80px;">${desc}</p>
            `;
            item.style.borderColor = "var(--accent-emerald)";
            item.style.background = "rgba(16, 185, 129, 0.05)";
        } else {
            item.innerHTML = `<p>${desc}</p>`;
        }
        container.appendChild(item);
    });
}

// Core Render logic for graphics (Only BST)
function renderStructureGraphic(visType) {
    if (!window.pywebview || !window.pywebview.api) return;

    if (visType === 'bst') {
        window.pywebview.api.obtener_arbol_estructura().then(root => {
            const wrapper = document.getElementById("bst-svg-wrapper");
            wrapper.innerHTML = "";
            if (!root) {
                wrapper.innerHTML = `<div style="padding:40px; text-align:center; color:var(--text-muted);">El catálogo está vacío. No hay libros registrados.</div>`;
                return;
            }

            // Render dynamic SVG
            const svgWidth = 900;
            const svgHeight = 450;
            const svgElements = [];
            
            // Recursive coordinate computer
            function drawNode(node, x, y, spacingX) {
                if (!node) return;
                
                // Draw lines first so they are behind circles
                if (node.izquierdo) {
                    const nextX = x - spacingX;
                    const nextY = y + 80;
                    svgElements.push(`<line x1="${x}" y1="${y}" x2="${nextX}" y2="${nextY}" stroke="var(--border-color)" stroke-width="2"/>`);
                    drawNode(node.izquierdo, nextX, nextY, spacingX * 0.48);
                }
                if (node.derecho) {
                    const nextX = x + spacingX;
                    const nextY = y + 80;
                    svgElements.push(`<line x1="${x}" y1="${y}" x2="${nextX}" y2="${nextY}" stroke="var(--border-color)" stroke-width="2"/>`);
                    drawNode(node.derecho, nextX, nextY, spacingX * 0.48);
                }

                const fill = node.estado === "Disponible" ? "var(--accent-emerald)" : "var(--accent-amber)";
                svgElements.push(`
                    <g class="tree-node" onclick="showBookDetail('${node.isbn}')">
                        <circle cx="${x}" cy="${y}" r="22" fill="var(--bg-secondary)" stroke="${fill}" stroke-width="3" style="filter: drop-shadow(0 0 6px ${fill}33);"/>
                        <text x="${x}" y="${y - 4}" text-anchor="middle" fill="var(--text-primary)" font-size="9" font-weight="bold" font-family="Outfit">${node.isbn}</text>
                        <text x="${x}" y="${y + 8}" text-anchor="middle" fill="var(--text-secondary)" font-size="7" font-family="Poppins">${node.titulo.substring(0, 10)}</text>
                    </g>
                `);
            }

            drawNode(root, svgWidth / 2, 40, svgWidth / 4);

            wrapper.innerHTML = `
                <svg width="100%" height="${svgHeight}" viewBox="0 0 ${svgWidth} ${svgHeight}" style="background:transparent; display:block;">
                    ${svgElements.join("")}
                </svg>
            `;
        });
    }
}

// Dialog Modal Operations
const overlay = document.getElementById("modal-overlay");
const mTitle = document.getElementById("modal-title");
const mBody = document.getElementById("modal-body");

function showModal(title, content) {
    mTitle.textContent = title;
    mBody.innerHTML = content;
    overlay.style.display = "flex";
}

function hideModal() {
    overlay.style.display = "none";
}

function closeModal(e) {
    hideModal();
}

// Show book visualizer click details
function showBookDetail(isbn) {
    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.buscar_libro("isbn", isbn).then(results => {
            if (results && results.length > 0) {
                const book = results[0];
                
                window.pywebview.api.obtener_cola_de_espera(isbn).then(cola => {
                    const colaCount = cola.length;
                    const isAvailable = book.estado === "Disponible";
                    
                    let modalContent = `
                        <div style="display:flex; flex-direction:column; gap:6px;">
                            <span style="font-family:Outfit; font-size:0.8rem; color:var(--accent-purple); font-weight:600;">ISBN: ${book.isbn}</span>
                            <h4 style="font-size:1.25rem; font-weight:700; color:var(--text-primary);">${book.titulo}</h4>
                            <p style="color:var(--text-secondary); font-size:0.9rem;">Autor: ${book.autor}</p>
                        </div>
                        <div style="display:flex; align-items:center; gap:8px;">
                            <span>Estado:</span>
                            <span class="book-badge ${book.estado}">${book.estado}</span>
                        </div>
                        <div class="glass-panel" style="padding:12px; background:rgba(255,255,255,0.02); font-size:0.85rem;">
                            <strong>Lista de Espera:</strong>
                            ${colaCount === 0 ? '<p style="color:var(--text-muted); margin-top:4px;">No hay personas en la lista de espera.</p>' : 
                            `<p style="color:var(--text-secondary); margin-top:4px;">Existen ${colaCount} ${colaCount === 1 ? 'persona' : 'personas'} en la lista de espera.</p>`}
                        </div>
                    `;

                    if (currentUser.role === "Bibliotecario") {
                        modalContent += `
                            <div style="display:flex; gap:10px; margin-top:10px;">
                                <button class="btn btn-secondary btn-danger" style="flex:1;" onclick="hideModal(); handleDeleteBook('${book.isbn}');">Eliminar Libro</button>
                                <button class="btn" style="flex:1.5;" onclick="hideModal(); showLoanReturnModal('${book.isbn}', '${book.titulo}', ${isAvailable});">
                                    ${isAvailable ? 'Registrar Préstamo' : 'Registrar Devolución'}
                                </button>
                            </div>
                        `;
                    } else {
                        modalContent += `
                            <div style="margin-top:10px;">
                                <button class="btn" style="width:100%;" onclick="hideModal(); handleClientRequestLoan('${book.isbn}');">
                                    ${isAvailable ? 'Solicitar Préstamo' : 'Unirse a Lista de Espera'}
                                </button>
                            </div>
                        `;
                    }

                    showModal("Detalles del Libro", modalContent);
                });
            }
        });
    }
}

// Show Add Book Panel
function showAddBookModal() {
    const formHtml = `
        <form id="add-book-form" onsubmit="handleAddBookSubmit(event)" style="display:flex; flex-direction:column; gap:16px;">
            <div class="form-group">
                <label for="new-isbn">ISBN del Libro</label>
                <input type="text" id="new-isbn" required placeholder="Ej. 9785">
            </div>
            <div class="form-group">
                <label for="new-titulo">Título</label>
                <input type="text" id="new-titulo" required placeholder="Ej. Hábitos Atómicos">
            </div>
            <div class="form-group">
                <label for="new-autor">Autor</label>
                <input type="text" id="new-autor" required placeholder="Ej. James Clear">
            </div>
            <button type="submit" class="btn" style="margin-top:10px;">Registrar Libro</button>
        </form>
    `;
    showModal("Registrar Nuevo Libro", formHtml);
}

// Submit add book
function handleAddBookSubmit(e) {
    e.preventDefault();
    const isbn = document.getElementById("new-isbn").value;
    const titulo = document.getElementById("new-titulo").value;
    const autor = document.getElementById("new-autor").value;

    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.registrar_libro(isbn, titulo, autor).then(response => {
            hideModal();
            if (response.success) {
                showToast(response.message, "success");
                refreshData();
            } else {
                showToast(response.message, "error");
            }
        });
    }
}

// Show Add User Panel
function showAddUserModal() {
    const formHtml = `
        <form id="add-user-form" onsubmit="handleAddUserSubmit(event)" style="display:flex; flex-direction:column; gap:16px;">
            <div class="form-group">
                <label for="new-user-id">Cédula / ID</label>
                <input type="text" id="new-user-id" required placeholder="Ej. C05">
            </div>
            <div class="form-group">
                <label for="new-user-nombre">Nombre Completo</label>
                <input type="text" id="new-user-nombre" required placeholder="Ej. Luis Zambrano">
            </div>
            <div class="form-group">
                <label for="new-user-correo">Correo Electrónico</label>
                <input type="email" id="new-user-correo" required placeholder="Ej. luis@correo.com">
            </div>
            <div class="form-group">
                <label for="new-user-pass">Contraseña</label>
                <input type="password" id="new-user-pass" required placeholder="••••••••">
            </div>
            <div class="form-group">
                <label for="new-user-rol">Rol del Usuario</label>
                <select id="new-user-rol" onchange="toggleEmployeeCodeField()" required>
                    <option value="Cliente">Cliente</option>
                    <option value="Bibliotecario">Bibliotecario (Librarian)</option>
                </select>
            </div>
            <div class="form-group" id="emp-code-group" style="display:none;">
                <label for="new-user-empcode">Código de Empleado</label>
                <input type="text" id="new-user-empcode" placeholder="Ej. EMP102">
            </div>
            <button type="submit" class="btn" style="margin-top:10px;">Registrar Usuario</button>
        </form>
    `;
    showModal("Registrar Nuevo Usuario", formHtml);
}

// Toggle employee code input in modal
function toggleEmployeeCodeField() {
    const rol = document.getElementById("new-user-rol").value;
    const group = document.getElementById("emp-code-group");
    if (rol === "Bibliotecario") {
        group.style.display = "flex";
        document.getElementById("new-user-empcode").required = true;
    } else {
        group.style.display = "none";
        document.getElementById("new-user-empcode").required = false;
    }
}

// Submit add user
function handleAddUserSubmit(e) {
    e.preventDefault();
    const id = document.getElementById("new-user-id").value;
    const nombre = document.getElementById("new-user-nombre").value;
    const correo = document.getElementById("new-user-correo").value;
    const pass = document.getElementById("new-user-pass").value;
    const rol = document.getElementById("new-user-rol").value;
    const empCode = document.getElementById("new-user-empcode").value || null;

    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.registrar_usuario(id, nombre, correo, pass, rol, empCode).then(response => {
            hideModal();
            if (response.success) {
                showToast(response.message, "success");
                refreshData();
            } else {
                showToast(response.message, "error");
            }
        });
    }
}

// Delete book handler
function handleDeleteBook(isbn) {
    if (confirm(`¿Está seguro de eliminar el libro con ISBN ${isbn} del catálogo?`)) {
        if (window.pywebview && window.pywebview.api) {
            window.pywebview.api.eliminar_libro(isbn).then(response => {
                if (response.success) {
                    showToast(response.message, "success");
                    refreshData();
                } else {
                    showToast(response.message, "error");
                }
            });
        }
    }
}

// Undo action handler
function handleUndo() {
    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.deshacer_ultima_accion().then(response => {
            if (response.success) {
                showToast(response.message, "success");
                refreshData();
            } else {
                showToast(response.message, "error");
            }
        });
    }
}

// Loan / Return modal for Librarian
function showLoanReturnModal(isbn, titulo, isAvailable) {
    let bodyHtml = '';
    
    if (isAvailable) {
        bodyHtml = `
            <form onsubmit="handleLibrarianLoanSubmit(event, '${isbn}')" style="display:flex; flex-direction:column; gap:16px;">
                <p style="font-size:0.9rem; color:var(--text-secondary);">El libro <strong>${titulo}</strong> está disponible. Registre el préstamo indicando el ID del cliente.</p>
                <div class="form-group">
                    <label for="loan-client-id">ID de Cliente (Cédula)</label>
                    <input type="text" id="loan-client-id" required placeholder="Ej. C01">
                </div>
                <button type="submit" class="btn">Prestar Libro</button>
            </form>
        `;
    } else {
        bodyHtml = `
            <form onsubmit="handleLibrarianReturnSubmit(event, '${isbn}')" style="display:flex; flex-direction:column; gap:16px;">
                <p style="font-size:0.9rem; color:var(--text-secondary);">El libro <strong>${titulo}</strong> está prestado. Registre la devolución indicando el ID del cliente que lo tiene prestado.</p>
                <div class="form-group">
                    <label for="return-client-id">ID de Cliente</label>
                    <input type="text" id="return-client-id" required placeholder="Ej. C01">
                </div>
                <button type="submit" class="btn btn-success">Registrar Devolución</button>
            </form>
        `;
    }
    showModal(isAvailable ? "Registrar Préstamo" : "Registrar Devolución", bodyHtml);
}

function handleLibrarianLoanSubmit(e, isbn) {
    e.preventDefault();
    const idCliente = document.getElementById("loan-client-id").value;
    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.realizar_prestamo(isbn, idCliente).then(response => {
            hideModal();
            if (response.success) {
                showToast(response.message, "success");
                refreshData();
            } else {
                showToast(response.message, "error");
            }
        });
    }
}

function handleLibrarianReturnSubmit(e, isbn) {
    e.preventDefault();
    const idCliente = document.getElementById("return-client-id").value;
    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.realizar_devolucion(isbn, idCliente).then(response => {
            hideModal();
            if (response.success) {
                showToast(response.message, "success");
                refreshData();
            } else {
                showToast(response.message, "error");
            }
        });
    }
}

// Client quick loans request
function handleClientRequestLoan(isbn) {
    if (!currentUser) return;
    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.realizar_prestamo(isbn, currentUser.idUsuario).then(response => {
            if (response.success) {
                showToast(response.message, "success");
                refreshData();
            } else {
                showToast(response.message, "error");
            }
        });
    }
}

// Client return loan
function handleClientReturnBook(isbn) {
    if (!currentUser) return;
    if (confirm("¿Confirmar devolución de este libro?")) {
        if (window.pywebview && window.pywebview.api) {
            window.pywebview.api.realizar_devolucion(isbn, currentUser.idUsuario).then(response => {
                if (response.success) {
                    showToast(response.message, "success");
                    refreshData();
                } else {
                    showToast(response.message, "error");
                }
            });
        }
    }
}

// Delete user (admin)
function handleDeleteUser(id, nombre) {
    if (confirm(`¿Está seguro de eliminar el usuario '${nombre}' (${id})?`)) {
        if (window.pywebview && window.pywebview.api) {
            window.pywebview.api.eliminar_usuario(id).then(response => {
                if (response.success) {
                    showToast(response.message, "success");
                    refreshData();
                } else {
                    showToast(response.message, "error");
                }
            });
        }
    }
}

// Load Global Loan History (Admin only)
function loadLoanHistory() {
    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.obtener_historial_prestamos_devoluciones().then(history => {
            renderLoanHistory(history);
        });
    }
}

// Render Global Loan History
function renderLoanHistory(history) {
    const container = document.getElementById("loan-history-list");
    if (!container) return;
    container.innerHTML = "";

    if (history.length === 0) {
        container.innerHTML = `<div style="text-align:center; color:var(--text-muted); padding: 20px;">No hay historial de préstamos o devoluciones registrado.</div>`;
        return;
    }

    history.forEach(desc => {
        const item = document.createElement("div");
        item.className = "stack-item";
        
        let iconHtml = "";
        let borderStyle = "";
        let bgStyle = "";
        
        if (desc.includes("Préstamo") || desc.includes("prestó")) {
            iconHtml = `<span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:var(--accent-amber); margin-right:8px;"></span>`;
            borderStyle = "1px solid rgba(245, 158, 11, 0.2)";
            bgStyle = "rgba(245, 158, 11, 0.03)";
        } else if (desc.includes("Devolución") || desc.includes("devuelto")) {
            iconHtml = `<span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:var(--accent-emerald); margin-right:8px;"></span>`;
            borderStyle = "1px solid rgba(16, 185, 129, 0.2)";
            bgStyle = "rgba(16, 185, 129, 0.03)";
        } else {
            iconHtml = `<span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:var(--accent-blue); margin-right:8px;"></span>`;
            borderStyle = "1px solid rgba(59, 130, 246, 0.2)";
            bgStyle = "rgba(59, 130, 246, 0.03)";
        }

        item.innerHTML = `<p style="display:flex; align-items:center; margin:0;">${iconHtml} ${desc}</p>`;
        item.style.border = borderStyle;
        item.style.background = bgStyle;
        container.appendChild(item);
    });
}
