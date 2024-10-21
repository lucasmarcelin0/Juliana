    document.addEventListener('DOMContentLoaded', function () {
        // Get the filter button and filter form container
        const filterButton = document.querySelector('.filter-button');
        const filterFormContainer = document.getElementById('filter-form-container');

        // Initialize the filter button toggle
        if (filterButton && filterFormContainer && (window.location.pathname === '/' || window.location.pathname.includes('index'))) {
            filterButton.addEventListener('click', function (event) {
                event.preventDefault(); // Prevent default behavior
                filterFormContainer.style.display = (filterFormContainer.style.display === 'none' || filterFormContainer.style.display === '') ? 'block' : 'none';
            });
        }

        // Initialize the apply filters button
        const applyFiltersButton = document.getElementById('apply-filters');
        if (applyFiltersButton) {
            applyFiltersButton.addEventListener('click', function () {
                console.log("Apply Filters button clicked."); // Log when button is clicked

                // Gather filter form data
                const formData = new FormData(document.getElementById('filter-form'));
                const queryParams = new URLSearchParams(formData).toString();
                const timestamp = new Date().getTime(); // Add timestamp to prevent caching
                const url = `/filter_properties/?${queryParams}&_=${timestamp}`;

                // Make the request using fetch
                fetch(url, {
                    method: 'GET',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => {
                    console.log('Fetch request completed with status:', response.status); // Log the status code
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error(`Server responded with status ${response.status}`);
                    }
                })
                .then(data => {
                    console.log('Fetch response data:', data); // Log the response data
                    renderProperties(data.properties);
                })
                .catch(error => {
                    console.error('Error loading properties:', error);
                });
            });
        }

        // Event delegation for details button click
        document.addEventListener('click', function (event) {
            if (event.target && event.target.classList.contains('details-button')) {
                const propertyId = event.target.getAttribute('data-id');
                toggleDetails(propertyId);
            }
        });
    });

    // Function to render properties in the container
    function renderProperties(properties) {
        const propertiesContainer = document.getElementById('properties-container');
        const renderedPropertyIds = new Set(); // Track already rendered properties to avoid duplicates

        if (propertiesContainer) {
            // Clear existing cards to avoid duplicates
            propertiesContainer.innerHTML = '';

            if (properties && properties.length > 0) {
                properties.forEach(property => {
                    // Skip rendering if the property is already in the set
                    if (renderedPropertyIds.has(property.id)) {
                        return;
                    }

                    renderedPropertyIds.add(property.id); // Add property ID to the set to track it
                    console.log('Appending property:', property);

                    const propertyCard = document.createElement('div');
                    propertyCard.classList.add('property-card');
                    propertyCard.setAttribute('id', `property-${property.id}`);

                    // Check if images exist, and if not, use a fallback
                    let propertyImagesHtml = '<p>No images available</p>';
                    if (property.images && Array.isArray(property.images) && property.images.length > 0) {
                        propertyImagesHtml = property.images.map((image, index) => {
                            return `<img src="${image.url}" alt="Property Image" class="property-image ${index === 0 ? 'first-image' : 'hidden'}">`;
                        }).join('');
                    }

                    // Set the HTML content of the property card
                    propertyCard.innerHTML = `
                        <div class="property-media">
                            <div class="property-photo" onclick="showAllImages(this)">
                                ${propertyImagesHtml}
                            </div>
                            <div class="property-video">
                                ${property.video_url ? `<iframe 
                                    src="${property.video_url}" 
                                    frameborder="0" 
                                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                                    allowfullscreen>
                                </iframe>` : '<p>Video Section Coming Soon</p>'}
                            </div>
                        </div>
                        <div class="property-info">
                            <p><strong>Endereço:</strong> ${property.street || 'Não especificado'}, ${property.street_number || 'N/A'}, ${property.neighborhood || 'N/A'}, ${property.city || 'N/A'}, ${property.state || 'N/A'}</p>
                            <p><strong>Preço:</strong> R$ ${property.sale_price || property.rent_price || 'N/A'}</p>
                            <p><strong>Alugar/Comprar:</strong> ${property.sale_price ? 'Comprar' : 'Alugar'}</p>
                        </div>
                        <button type="button" class="details-button" data-id="${property.id}">Ver mais detalhes</button>
                        <div id="additional-info-${property.id}" class="property-info hidden">
                            <p><strong>Área do Imóvel:</strong> ${property.property_area || 'N/A'} m²</p>
                            <p><strong>Quartos:</strong> ${property.bedrooms || 'N/A'}</p>
                            <p><strong>Suítes:</strong> ${property.suites || 'N/A'}</p>
                            <p><strong>Banheiros:</strong> ${property.bathrooms || 'N/A'}</p>
                            <p><strong>Características:</strong> ${property.features || 'N/A'}</p>
                            <p><strong>Área Privativa:</strong> ${property.private_area || 'N/A'} m²</p>
                            <p><strong>Vagas de Garagem:</strong> ${property.garage_spots || 'N/A'}</p>
                            <p><strong>Tipo de Garagem:</strong> ${property.garage_type || 'N/A'}</p>
                            <p><strong>Tem Piscina:</strong> ${property.has_pool ? 'Sim' : 'Não'}</p>
                            <p><strong>Portaria:</strong> ${property.has_gatehouse || 'N/A'}</p>
                            <p><strong>Condição:</strong> ${property.is_occupied || 'N/A'}</p>
                            <p><strong>Acessibilidade:</strong> ${property.accessibility || 'N/A'}</p>
                            <p><strong>Data de Disponibilidade para Mudança:</strong> ${property.move_availability || 'N/A'}</p>
                            <p><strong>Preço do Aluguel:</strong> R$ ${property.rent_price || 'N/A'}</p>
                            <p><strong>Preço de Venda:</strong> R$ ${property.sale_price || 'N/A'}</p>
                            <p><strong>Valor do IPTU:</strong> R$ ${property.iptu_value || 'N/A'}</p>
                            <p><strong>Taxa de Condomínio:</strong> R$ ${property.condo_fee || 'N/A'}</p>
                            <p><strong>Descrição Livre:</strong> ${property.free_description || 'N/A'}</p>
                        </div>
                    `;

                    // Append the card to the container
                    propertiesContainer.appendChild(propertyCard);
                });
            } else {
                console.warn('No properties found.');
                propertiesContainer.innerHTML = '<p>No properties matched your criteria.</p>';
            }
        }
    }

    function showAllImages(element) {
        const images = element.querySelectorAll('.property-image:not(.first-image)');
        const currentlyVisible = Array.from(images).every(img => !img.classList.contains('hidden'));

        images.forEach((img) => {
            img.classList.toggle('hidden', currentlyVisible);
        });

        if (!currentlyVisible) {
            openFullscreenModal(element);
        }

        element.style.cursor = currentlyVisible ? 'pointer' : 'zoom-out';
    }

    function openFullscreenModal(element) {
        const modal = document.getElementById("fullscreen-modal");
        const modalContent = document.getElementById("modal-content");

        // Clear any previous content in the modal
        modalContent.innerHTML = "";

        // Add all images from the clicked container to the modal
        const images = element.querySelectorAll('.property-image');
        images.forEach((img) => {
            const modalImg = img.cloneNode(true);
            modalContent.appendChild(modalImg);
        });

        // Show the modal
        modal.style.display = "block";
    }

    function closeFullscreen() {
        const modal = document.getElementById("fullscreen-modal");
        modal.style.display = "none";
    }

    function toggleDetails(counter) {
        console.log("Toggle ID: ", counter);
        const additionalInfo = document.getElementById(`additional-info-${counter}`);
        if (additionalInfo) {
            additionalInfo.classList.toggle('hidden');
        } else {
            console.error('Element not found for ID:', counter);
        }
    }
