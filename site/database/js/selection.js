/**
 * selection.js - Gerenciamento de Seleção e Atalhos de Teclado
 * Responsável por: seleção de arquivos, CTRL+A/C/V, clipboard interno, download de pastas como ZIP
 * OTIMIZADO: Compactação agora ocorre no servidor para melhor performance
 */

function isItemSelected(id) {
    return selectedFiles.includes(id) || isContainedInSelectedFolder(id);
}

function getParentPath(id) {
    for (const parentPath in fileStructure) {
        const entry = fileStructure[parentPath];
        if (entry.files?.some(f => f.id === id) || entry.folders?.some(f => f.id === id)) {
            return parentPath;
        }
    }
    return null;
}

function checkAndBubbleSelection(id) {
    const parentPath = getParentPath(id);
    if (!parentPath || parentPath === "database_root") return;
    
    const parentEntry = fileStructure[parentPath];
    if (!parentEntry) return;

    const children = [
        ...(parentEntry.folders || []).map(f => f.id),
        ...(parentEntry.files || []).map(f => f.id)
    ];

    if (children.length === 0) return;

    // Verifica se todos os filhos estão selecionados (explícita ou implicitamente)
    const allChildrenSelected = children.every(childId => isItemSelected(childId));

    if (allChildrenSelected) {
        // Remove todos os filhos de selectedFiles
        selectedFiles = selectedFiles.filter(selId => !children.includes(selId));
        // Adiciona o pai a selectedFiles
        if (!selectedFiles.includes(parentPath)) {
            selectedFiles.push(parentPath);
        }
        // Verifica recursivamente o pai
        checkAndBubbleSelection(parentPath);
    }
}

function selectItem(id) {
    if (isItemSelected(id)) return;

    // Como estamos selecionando este item, removemos quaisquer descendentes explicitamente selecionados
    selectedFiles = selectedFiles.filter(selId => !selId.startsWith(id + '/'));

    selectedFiles.push(id);

    // Borbulha a seleção para os pais
    checkAndBubbleSelection(id);
}

function selectSiblingsExcept(folderId, targetId) {
    const entry = fileStructure[folderId];
    if (!entry) return;
    const children = [
        ...(entry.folders || []),
        ...(entry.files || [])
    ];
    for (const child of children) {
        if (child.id === targetId) {
            continue;
        }
        if (targetId.startsWith(child.id + '/')) {
            // O alvo de desmarcação está dentro desta pasta, entra recursivamente para selecionar seus irmãos
            selectSiblingsExcept(child.id, targetId);
        } else {
            // Arquivo/pasta irmão do caminho do alvo, mantém selecionado
            if (!selectedFiles.includes(child.id)) {
                selectedFiles.push(child.id);
            }
        }
    }
}

function deselectItem(id) {
    const idx = selectedFiles.indexOf(id);
    if (idx !== -1) {
        selectedFiles.splice(idx, 1);
        // Também remove descendentes, por segurança
        selectedFiles = selectedFiles.filter(selId => !selId.startsWith(id + '/'));
        return;
    }

    // Se estiver selecionado implicitamente, encontra o ancestral que está em selectedFiles
    let ancestorId = null;
    for (const selId of selectedFiles) {
        if (id.startsWith(selId + '/')) {
            ancestorId = selId;
            break;
        }
    }

    if (ancestorId) {
        const aIdx = selectedFiles.indexOf(ancestorId);
        if (aIdx !== -1) {
            selectedFiles.splice(aIdx, 1);
        }
        selectSiblingsExcept(ancestorId, id);
    }
}

function toggleSelection(id) {
    if (isItemSelected(id)) {
        deselectItem(id);
    } else {
        selectItem(id);
    }
    renderFiles();
}

function selectAll() {
    files.forEach(f => selectItem(f.id));
    renderFiles();
}

function clearSelection() {
    selectedFiles = [];
    renderFiles();
}

async function downloadSelected() {
    if (selectedFiles.length === 0) return;

    // Separar arquivos e pastas
    const filesToDownload = [];
    const foldersToDownload = [];

    for (const id of selectedFiles) {
        const file = findFileById(id);
        if (file) {
            if (file.isDirectory) {
                foldersToDownload.push(file);
            } else {
                filesToDownload.push(file);
            }
        }
    }

    // Se houver apenas 1 arquivo e nenhuma pasta, baixar diretamente
    if (filesToDownload.length === 1 && foldersToDownload.length === 0) {
        showNotification(`Baixando ${filesToDownload[0].name}...`, "info");
        const a = document.createElement('a');
        a.href = "/" + filesToDownload[0].path;
        a.download = filesToDownload[0].name;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        showNotification(`${filesToDownload[0].name} baixado!`, "success");
        registrarLogDownload(filesToDownload, "arquivos");
        return;
    }

    // Se houver múltiplos arquivos ou pastas, usar compactação no servidor
    showNotification("Preparando download (compactando no servidor)...", "info");
    await downloadZipFromServer(foldersToDownload, filesToDownload);
}

async function downloadZipFromServer(folders, files) {
    try {
        // Preparar lista de caminhos
        // O zip_manager recebe caminhos relativos ao DATABASE_DIR (ex: "files/dev")
        // mas file.path e folder.path têm o prefixo "database/" (ex: "database/files/dev")
        // Precisamos remover o prefixo "database/" antes de enviar
        const paths = [];
        
        for (const file of files) {
            const p = file.path.startsWith('database/') ? file.path.slice('database/'.length) : file.path;
            paths.push(p);
        }
        
        for (const folder of folders) {
            const p = folder.path.startsWith('database/') ? folder.path.slice('database/'.length) : folder.path;
            paths.push(p);
        }

        // Enviar requisição POST para o servidor
        const response = await fetch('/database/download-zip', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ paths: paths })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Erro ao compactar');
        }

        // Obter o blob do ZIP
        const blob = await response.blob();
        const zipUrl = URL.createObjectURL(blob);
        
        // Criar link e fazer download
        const a = document.createElement('a');
        a.href = zipUrl;
        a.download = `download_${new Date().getTime()}.zip`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(zipUrl);

        showNotification("✅ Download concluído com sucesso!", "success");
        registrarLogDownload(folders, "pastas");
    } catch (error) {
        console.error("Erro ao fazer download:", error);
        showNotification(`❌ Erro ao fazer download: ${error.message}`, "error");
    }
}

function registrarLogDownload(items, tipo) {
    const timestamp = new Date().toLocaleString('pt-BR');
    const nomes = items.map(i => i.name).join(", ");
    const logMsg = `[${timestamp}] Download de ${tipo}: ${nomes}`;
    console.log(logMsg);
    // Aqui você pode enviar para o servidor se necessário
}

function shareSelected() {
    if (selectedFiles.length === 0) return;
    const shareUrl = window.location.origin + window.location.pathname + "?share=" + selectedFiles.join(",");
    navigator.clipboard.writeText(shareUrl).then(() => {
        showNotification("Link copiado para a área de transferência!", "success");
    });
}

// ── Atalhos de teclado: CTRL+A, CTRL+C, CTRL+V ─────────────────────────────
function handleKeyboardShortcuts(e) {
    // Ignorar quando o foco está em inputs, textareas ou modais abertos
    const tag = document.activeElement.tagName.toLowerCase();
    if (tag === "input" || tag === "textarea" || tag === "select") return;
    if (elements.uploadModal && elements.uploadModal.style.display !== "none") return;
    if (elements.previewModal && elements.previewModal.style.display !== "none") return;

    const isCtrl = e.ctrlKey || e.metaKey;

    if (isCtrl && e.key === "a") {
        e.preventDefault();
        selectAll();
        showNotification("Todos os arquivos selecionados", "info");
    }

    if (isCtrl && e.key === "c") {
        if (selectedFiles.length === 0) return;
        e.preventDefault();
        clipboardFiles = [...selectedFiles];
        showNotification(`${clipboardFiles.length} arquivo(s) copiado(s) para a área de transferência`, "success");
    }

    if (isCtrl && e.key === "v") {
        if (clipboardFiles.length === 0) return;
        e.preventDefault();
        pasteFiles();
    }
}

// Cola os arquivos copiados na pasta atual (download dos arquivos selecionados como ação de "colar")
function pasteFiles() {
    if (clipboardFiles.length === 0) {
        showNotification("Nenhum arquivo na área de transferência", "warning");
        return;
    }

    let pasted = 0;
    for (const id of clipboardFiles) {
        const file = findFileById(id);
        if (file && !file.isDirectory) {
            const a = document.createElement('a');
            a.href = "/" + file.path;
            a.download = file.name;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            pasted++;
        }
    }

    if (pasted > 0) {
        showNotification(`${pasted} arquivo(s) colado(s) (download iniciado)`, "success");
    } else {
        showNotification("Nenhum arquivo válido para colar", "warning");
    }
}
