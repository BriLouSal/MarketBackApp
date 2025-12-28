

// Now we wanna create a UI Client Side to create for 

// Fix these syntax errors later
const ctx = document.getElementById('stockGraph').getContext('2d');

// Graph for the Stock
let myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: chartLabels, // From my Django connected via stock.html
        datasets: [{
            label: `${stockTicker} Price`,
            data: chartPrices, 
            borderColor: '#3b82f6',
            fill: true,
            tension: 0.1,
            backgroundColor: '#2d485c',
        }]
    },
    options: {
        responsive: true,          
        maintainAspectRatio: false, 
    }
});



// Buttoms
const buttons = document.querySelectorAll('.interval')

function buttonUpdate() {
    buttons.forEach(btn =>{
    btn.addEventListener('click', function() {
        buttons.forEach(b => {
            
            b.classList.remove('bg-blue-500'); 
            b.classList.add('bg-blue-800');
            b.classList.add('text-gray-950');
        });
            this.classList.remove('bg-blue-800');
            this.classList.add('bg-blue-500');
            this.classList.add('text-white');
        });
    });

}
buttonUpdate();

// 1. Select the buttons using the class you defined in HTML
