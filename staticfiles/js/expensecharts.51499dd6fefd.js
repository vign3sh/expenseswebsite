function make_dashboard(){

  var exp=[document.getElementById("today_exp"), document.getElementById("week_exp"),
            document.getElementById("month_exp"), document.getElementById("year_exp")]

  var c=[document.getElementById("today_count"),document.getElementById("week_count"),
            document.getElementById("month_count"),document.getElementById("year_count")]

  fetch("/expense_dashboard")
    .then((res) => res.json())
    .then((results) => {
      const amount = results.amount;
      const count=results.count

      for (let i = 0; i < 4; i++) {
        exp[i].innerHTML+=amount[i];
        c[i].innerHTML=count[i]; 
      }



    });
}


const renderChart = (data, labels) => {
  var ctx = document.getElementById("month_chart").getContext("2d");
  var myChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          fill: true,
          data: data,
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)"            
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)"        
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      plugins: {
      title: {
        display: true,
        text: "Monthly Expense",
      },
    }
    },
  });
};

const getChartData = () => {

  fetch("/expense_summary")
    .then((res) => res.json())
    .then((results) => {
      
      const category_data = results.month;
      const [labels, data] = [
        Object.keys(category_data),
        Object.values(category_data),
      ];
    renderChart(data, labels);
    });
};
document.onload = make_dashboard()
document.onload = getChartData()
