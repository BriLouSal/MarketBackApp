

// Now we wanna create a UI Client Side to create for 

const stock_graph = document.getElementById('stockGraph').getContext('2d');



const gradient = ctx.createLinearGradient(0, 0, 0, 400);
gradient.addColorStop(0, 'rgba(30, 58, 138, 0.2)'); 
gradient.addColorStop(1, 'rgba(30, 58, 138, 0)');



  new Chart(stock_graph, {
    type: 'line',
    data: {
      labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
      datasets: [{
        label: ${chartLabels},
        data: [12, 19, 3, 5, 2, 3],
        borderWidth: 1,
        
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });


// Buttoms
const buttons = document.querySelectorAll('.interval')

buttons.forEach(btn =>{
    btn.addEventListener('click', function() {

    })
})