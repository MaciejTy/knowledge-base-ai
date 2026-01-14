// API Base URL
const API_URL = '/api/documents';

// Current document being viewed
let currentDocument = null;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    loadDocuments();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // New document button
    document.getElementById('newDocBtn').addEventListener('click', showNewDocumentModal);

    // New document form
    document.getElementById('newDocForm').addEventListener('submit', handleCreateDocument);

    // Search input
    document.getElementById('searchInput').addEventListener('input', handleSearch);
}

// Load all documents
async function loadDocuments() {
    showLoading();

    try {
        const response = await fetch(API_URL);
        const documents = await response.json();

        hideLoading();

        if (documents.length === 0) {
            showEmptyState();
        } else {
            hideEmptyState();
            renderDocuments(documents);
        }
    } catch (error) {
        hideLoading();
        showToast('Error loading documents', 'error');
        console.error('Error:', error);
    }
}

// Render documents grid
function renderDocuments(documents) {
    const grid = document.getElementById('documentsGrid');
    grid.innerHTML = '';

    documents.forEach(doc => {
        const card = createDocumentCard(doc);
        grid.appendChild(card);
    });
}

// Create document card
function createDocumentCard(doc) {
    const card = document.createElement('div');
    card.className = 'bg-white/5 backdrop-blur-md border border-purple-500/20 rounded-xl p-6 hover:border-purple-500/50 transition-all cursor-pointer transform hover:scale-[1.02] hover:shadow-xl hover:shadow-purple-500/20';
    card.onclick = () => showDocumentDetail(doc.id);

    const tags = doc.tags && doc.tags.length > 0
        ? doc.tags.slice(0, 3).map(tag =>
            `<span class="px-3 py-1 bg-purple-500/20 text-purple-300 rounded-full text-xs font-semibold">${tag}</span>`
          ).join('')
        : '<span class="text-gray-500 text-xs">No tags</span>';

    const summary = doc.summary
        ? `<p class="text-gray-300 text-sm line-clamp-3">${doc.summary}</p>`
        : `<p class="text-gray-400 text-sm line-clamp-3">${doc.content.substring(0, 150)}...</p>`;

    card.innerHTML = `
        <div class="flex items-start justify-between mb-3">
            <h3 class="text-xl font-bold text-white flex-1 line-clamp-2">${doc.title}</h3>
            <i class="fas fa-chevron-right text-purple-400 ml-2"></i>
        </div>

        <div class="flex flex-wrap gap-2 mb-3">
            ${tags}
        </div>

        ${summary}

        <div class="mt-4 pt-4 border-t border-purple-500/10 flex items-center justify-between text-xs text-gray-400">
            <span><i class="far fa-calendar mr-1"></i>${formatDate(doc.created_at)}</span>
            <span><i class="fas fa-file-alt mr-1"></i>${doc.source_type}</span>
        </div>
    `;

    return card;
}

// Show document detail
async function showDocumentDetail(id) {
    try {
        const response = await fetch(`${API_URL}/${id}`);
        currentDocument = await response.json();

        document.getElementById('detailTitle').textContent = currentDocument.title;

        // Tags
        const tagsContainer = document.getElementById('detailTags');
        if (currentDocument.tags && currentDocument.tags.length > 0) {
            tagsContainer.innerHTML = currentDocument.tags.map(tag =>
                `<span class="px-4 py-2 bg-purple-500/20 text-purple-300 rounded-full text-sm font-semibold">${tag}</span>`
            ).join('');
        } else {
            tagsContainer.innerHTML = '<span class="text-gray-500 text-sm">No tags</span>';
        }

        // Summary
        const summarySection = document.getElementById('detailSummarySection');
        if (currentDocument.summary) {
            summarySection.style.display = 'block';
            document.getElementById('detailSummary').textContent = currentDocument.summary;
        } else {
            summarySection.style.display = 'none';
        }

        // Content
        document.getElementById('detailContent').textContent = currentDocument.content;

        // Show modal
        document.getElementById('detailModal').classList.remove('hidden');
        document.getElementById('detailModal').classList.add('flex');
    } catch (error) {
        showToast('Error loading document', 'error');
        console.error('Error:', error);
    }
}

// Close detail modal
function closeDetailModal() {
    document.getElementById('detailModal').classList.add('hidden');
    document.getElementById('detailModal').classList.remove('flex');
    currentDocument = null;
}

// Show new document modal
function showNewDocumentModal() {
    document.getElementById('newDocModal').classList.remove('hidden');
    document.getElementById('newDocModal').classList.add('flex');
    document.getElementById('docTitle').focus();
}

// Close new document modal
function closeNewDocumentModal() {
    document.getElementById('newDocModal').classList.add('hidden');
    document.getElementById('newDocModal').classList.remove('flex');
    document.getElementById('newDocForm').reset();
}

// Handle create document
async function handleCreateDocument(e) {
    e.preventDefault();

    const title = document.getElementById('docTitle').value;
    const content = document.getElementById('docContent').value;

    // Show creating indicator
    document.getElementById('creatingIndicator').classList.remove('hidden');

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title,
                content,
                source_type: 'manual'
            })
        });

        if (!response.ok) {
            throw new Error('Failed to create document');
        }

        const newDoc = await response.json();

        // Hide indicator
        document.getElementById('creatingIndicator').classList.add('hidden');

        // Close modal
        closeNewDocumentModal();

        // Show success toast
        showToast('Document created with AI! 🤖', 'success');

        // Reload documents
        await loadDocuments();

        // Show new document detail
        setTimeout(() => showDocumentDetail(newDoc.id), 500);

    } catch (error) {
        document.getElementById('creatingIndicator').classList.add('hidden');
        showToast('Error creating document', 'error');
        console.error('Error:', error);
    }
}

// Regenerate AI
async function regenerateAI() {
    if (!currentDocument) return;

    const btn = document.getElementById('regenerateBtn');
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Regenerating...';

    try {
        const response = await fetch(`${API_URL}/${currentDocument.id}/regenerate-ai`, {
            method: 'POST'
        });

        if (!response.ok) {
            throw new Error('Failed to regenerate');
        }

        const updatedDoc = await response.json();

        showToast('AI content regenerated! 🔄', 'success');

        // Reload documents and show updated detail
        await loadDocuments();
        await showDocumentDetail(updatedDoc.id);

    } catch (error) {
        showToast('Error regenerating AI', 'error');
        console.error('Error:', error);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-sync-alt mr-2"></i>Regenerate AI';
    }
}

// Delete document
async function deleteDocument() {
    if (!currentDocument) return;

    if (!confirm('Are you sure you want to delete this document?')) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/${currentDocument.id}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error('Failed to delete');
        }

        closeDetailModal();
        showToast('Document deleted', 'success');
        await loadDocuments();

    } catch (error) {
        showToast('Error deleting document', 'error');
        console.error('Error:', error);
    }
}

// Handle search
let searchTimeout;
function handleSearch(e) {
    clearTimeout(searchTimeout);

    const query = e.target.value.trim();

    if (query === '') {
        loadDocuments();
        return;
    }

    searchTimeout = setTimeout(async () => {
        try {
            const response = await fetch(`${API_URL}/search?q=${encodeURIComponent(query)}`);
            const documents = await response.json();

            if (documents.length === 0) {
                document.getElementById('documentsGrid').innerHTML = `
                    <div class="col-span-full text-center py-20">
                        <i class="fas fa-search text-6xl text-purple-400/50 mb-4"></i>
                        <h3 class="text-2xl font-semibold text-gray-300 mb-2">No results found</h3>
                        <p class="text-gray-400">Try a different search term</p>
                    </div>
                `;
            } else {
                renderDocuments(documents);
            }
        } catch (error) {
            showToast('Error searching', 'error');
            console.error('Error:', error);
        }
    }, 300);
}

// Show/hide loading
function showLoading() {
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('documentsGrid').classList.add('hidden');
}

function hideLoading() {
    document.getElementById('loading').classList.add('hidden');
    document.getElementById('documentsGrid').classList.remove('hidden');
}

// Show/hide empty state
function showEmptyState() {
    document.getElementById('emptyState').classList.remove('hidden');
    document.getElementById('documentsGrid').classList.add('hidden');
}

function hideEmptyState() {
    document.getElementById('emptyState').classList.add('hidden');
    document.getElementById('documentsGrid').classList.remove('hidden');
}

// Show toast notification
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const icon = document.getElementById('toastIcon');
    const msg = document.getElementById('toastMessage');

    msg.textContent = message;

    if (type === 'error') {
        icon.className = 'fas fa-exclamation-circle text-xl';
        toast.className = 'fixed bottom-6 right-6 bg-gradient-to-r from-red-500 to-pink-500 text-white px-6 py-4 rounded-lg shadow-2xl transform transition-all';
    } else {
        icon.className = 'fas fa-check-circle text-xl';
        toast.className = 'fixed bottom-6 right-6 bg-gradient-to-r from-purple-500 to-pink-500 text-white px-6 py-4 rounded-lg shadow-2xl transform transition-all';
    }

    toast.classList.remove('hidden');

    setTimeout(() => {
        toast.classList.add('hidden');
    }, 3000);
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}