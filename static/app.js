// Function to fetch and display cupcakes
function fetchCupcakes() {
    axios.get('/api/cupcakes')
        .then(response => {
            const cupcakes = response.data.cupcakes;
            const cupcakeList = $('#cupcake-list');
            cupcakeList.empty(); // Clear the current list

            cupcakes.forEach(cupcake => {
                cupcakeList.append(`
                    <div class="cupcake-item">
                        <h3>${cupcake.flavor} (${cupcake.size})</h3>
                        <p>Rating: ${cupcake.rating}</p>
                        <img src="${cupcake.image}" alt="${cupcake.flavor} cupcake" width="100">
                    </div>
                `);
            });
        })
        .catch(error => console.error('Error fetching cupcakes:', error));
}

// Handle form submission
$('#cupcake-form').on('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    const newCupcake = {
        flavor: $('#flavor').val(),
        size: $('#size').val(),
        rating: parseFloat($('#rating').val()),
        image: $('#image').val() || 'https://tinyurl.com/demo-cupcake' // Default image if not provided
    };

    axios.post('/api/cupcakes', newCupcake)
        .then(response => {
            const cupcake = response.data.cupcake;
            $('#cupcake-list').append(`
                <div class="cupcake-item">
                    <h3>${cupcake.flavor} (${cupcake.size})</h3>
                    <p>Rating: ${cupcake.rating}</p>
                    <img src="${cupcake.image}" alt="${cupcake.flavor} cupcake" width="100">
                </div>
            `);
            // Clear the form
            $('#cupcake-form')[0].reset();
        })
        .catch(error => console.error('Error adding cupcake:', error));
});

// Fetch cupcakes on page load
$(document).ready(fetchCupcakes);
