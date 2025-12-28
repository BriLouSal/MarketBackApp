

// Now we wanna create a UI Client Side to create for 

// Fix these syntax errors later
// const ctx = document.getElementById('stockGraph').getContext('2d');
// let myChart = new myChart(ctx, {
//     type: 'line',
//     data: {
//         labels: chartLabels,
//         datasets: [{
//             label: `${stockTicker} Price`,
//             data: chartPrices,
//             borderColor: '#3b82f6',
//             fill: false,
//             tension: 0.1
//         }]
//     }
// });;




// Buttoms
const buttons = document.querySelectorAll('.interval')

function buttonUpdate() {
    buttons.forEach(btn =>{
    btn.addEventListener('click', function() {
        buttons.forEach(b => {
            // Not inactive anymore
            b.classList.remove('bg-blue-500') 
            b.classList.add('bg-blue-800')
        })
        this.classList.remove('bg-blue-500')
        this.classList.add('bg-blue-800')
    })
})

}
buttonUpdate();
console.log("Test!");