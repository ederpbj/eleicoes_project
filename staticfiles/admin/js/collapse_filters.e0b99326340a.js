document.addEventListener('DOMContentLoaded', function () {
    const filterBox = document.querySelector('.module .filter');
    if (filterBox) {
        // Cria um botão de colapso
        const toggleButton = document.createElement('button');
        toggleButton.textContent = 'Mostrar/Ocultar Filtros';
        toggleButton.style.marginBottom = '10px';
        toggleButton.style.cursor = 'pointer';
        toggleButton.classList.add('btn', 'btn-default');

        // Adiciona o botão antes dos filtros
        filterBox.parentNode.insertBefore(toggleButton, filterBox);

        // Adiciona o evento de clique para esconder/mostrar os filtros
        toggleButton.addEventListener('click', function () {
            filterBox.style.display = filterBox.style.display === 'none' ? 'block' : 'none';
        });

        // Começa com os filtros ocultos (opcional)
        filterBox.style.display = 'none';
    }
});
