const { createElement } = require("react");





const message = document.createElement('div');




message.classList('gen-ai')

message.innerText = "";


document.addEventListener('DOMContentLoaded', () => {
  const genAiElement = document.getElementById('gen-ai-text');
  const content = genAiElement.getAttribute('data-content');



  let index = 0;
  function typeWriter() {
    if (index < content.length) {
      genAiElement.innerHTML += content.charAt(index);
      index++;
      setTimeout(typeWriter, 15); // Speed of animation
    }
  }

  typeWriter(); // Start animation on page load
});




const stock_graph = document.getElementsByClassName('stock_graph')


// Get JSON data



// Stocks

async function Chart() {
  const stock = "{{ request.resolver_match.kwargs.stock_tick }}";
  const response = await fetch(`/api/stock/${stock}/`);
  const data = await response.json();

  const ctx = document.getElementById('chart').getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.dates,
      datasets: [{
        label: `${stock} Closing Price`,
        data: data.prices,
        borderWidth: 2,
        fill: false
      }]
    },
  });
}

loadChart();




