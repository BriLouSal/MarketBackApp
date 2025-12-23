

// Now we wanna create a UI Client Side to create for 

const stock_graph = document.getElementById('stock_graph').getContext('2d');



const gradient = ctx.createLinearGradient(0, 0, 0, 400);
gradient.addColorStop(0, 'rgba(30, 58, 138, 0.2)'); 
gradient.addColorStop(1, 'rgba(30, 58, 138, 0)');