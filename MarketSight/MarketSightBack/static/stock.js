

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
        scales: {
            x: {
                ticks : {
                    maxTicksLimit: 10,
                    autoSkip: true

                },
                grid: {
                    display: false

                }
            }

        },
    }
});



// Buttoms
const buttons = document.querySelectorAll('.interval')

function buttonUpdate() {
    buttons.forEach(btn => {
        btn.addEventListener('click', function() {
            buttons.forEach(b => {
                b.classList.remove('bg-blue-500', 'text-white'); 
                b.classList.add('bg-blue-800', 'text-gray-950');
            });

            this.classList.remove('bg-blue-800', 'text-gray-950');
            this.classList.add('bg-blue-500', 'text-white');

            const interval = this.getAttribute('data-interval');
            console.log("Fetching data for:", interval);
        });
    });
}
buttonUpdate();




// Grab the Card div to create a gsap animation

const cards = document.querySelectorAll('.flexcard')



gsap.from(cards, {
    opactiy: 0,
    y: 50,
    duration: 4,
    ease: 'power3.out',
})