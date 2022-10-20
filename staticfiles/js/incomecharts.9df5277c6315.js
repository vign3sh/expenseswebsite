function make_dashboard(){

    var exp=[document.getElementById("today_exp"), document.getElementById("week_exp"),
              document.getElementById("month_exp"), document.getElementById("year_exp")]
  
    var c=[document.getElementById("today_count"),document.getElementById("week_count"),
              document.getElementById("month_count"),document.getElementById("year_count")]
  
    fetch("/income/income_dashboard")
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
  
  
  const renderChart = (chart_name,data, labels, title, backc, borc) => {
    var ctx = document.getElementById(chart_name).getContext("2d");
    var myChart = new Chart(ctx, {
      type: "line",
      data: {
        labels: labels,
        datasets: [
          {
            fill: true,
            lineTension: 0.4,
            data: data,
            backgroundColor: [
              backc            
            ],
            borderColor: [
              borc        
            ],
            borderWidth: 1,
          },
        ],
      },
      options: {
        plugins: {
        title: {
          display: true,
          text: title,
        },
      }
      },
    });
  };
  
  const getChartData = () => {
  
    fetch("/income/income_summary")
      .then((res) => res.json())
      .then((results) => {
        
        const category_data = results.month;
        const year_data = results.year;
        const [labels, data] = [
          Object.keys(category_data),
          Object.values(category_data),
        ];
        const [y_labels, y_data] = [
          Object.keys(year_data),
          Object.values(year_data),
        ];
  
      renderChart('month_chart',data, labels, "Monthly Expense", "rgba(255, 99, 132, 0.2)","rgba(255, 99, 132, 1)");
      renderChart('year_chart',y_data,y_labels,"Yearly Expense", "rgba(75, 192, 192, 0.2)","rgba(75, 192, 192, 1)");
  
      });
  };
  document.onload = make_dashboard()
  document.onload = getChartData()
  