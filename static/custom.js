let chart;

// Fetch crop data from Flask API
async function fetchCropData() {
  try {
    const response = await fetch('/api/get_crop_data');
    const data = await response.json();

    if (data.length === 0) {
      document.getElementById('chartPlaceholder').style.display = 'block';  // Show placeholder text if no data
    } else {
      document.getElementById('chartPlaceholder').style.display = 'none';  // Hide placeholder text
      renderChart(data);
    }
  } catch (error) {
    console.error("Error fetching crop data:", error);
  }
}

// Function to render the chart
function renderChart(data) {
  const ctx = document.getElementById('cropChart').getContext('2d');
  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.map(item => item.date),
      datasets: [{
        label: 'Crop Price',
        data: data.map(item => item.price),
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        fill: false,
        tension: 0.1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { title: { display: true, text: 'Date' } },
        y: { title: { display: true, text: 'Price' }, beginAtZero: false }
      }
    }
  });
}

fetchCropData();  // Fetch the data and render the chart
