const renderChart = (data, labels) => {
    var ctx = document.getElementById("donutchart").getContext("2d");
    if(window.myCharts != undefined){
      window.myCharts.destroy();
    }
    window.myCharts =  new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Last 6 months Income",
            data: data,
            backgroundColor: [
              "rgba(255, 99, 132, 0.2)",
              "rgba(54, 162, 235, 0.2)",
              "rgba(255, 206, 86, 0.2)",
              "rgba(75, 192, 192, 0.2)",
              "rgba(153, 102, 255, 0.2)",
              "rgba(255, 159, 64, 0.2)",
            ],
            borderColor: [
              "rgba(255, 99, 132, 1)",
              "rgba(54, 162, 235, 1)",
              "rgba(255, 206, 86, 1)",
              "rgba(75, 192, 192, 1)",
              "rgba(153, 102, 255, 1)",
              "rgba(255, 159, 64, 1)",
            ],
            borderWidth: 1,
          },
        ],
      },
      options: {
        plugins: {
        title: {
          display: true,
          text: "Income per category(Last 6 months)",
        },
      }
      },
    });
  };
  
  const getChartData = () => {
    console.log("fetching");
    fetch("/income/income_category_summary")
      .then((res) => res.json())
      .then((results) => {
        console.log("results", results);
        const category_data = results.expense_category_data;
        const [labels, data] = [
          Object.keys(category_data),
          Object.values(category_data),
        ];
  
        renderChart(data, labels);
      });
  };
  
  const renderChart2 = (data, labels, months) => {


    var speedCanvas = document.getElementById("linechart");
    
  
   var datasets=[];
    const backgroundColor= [
      "rgba(255, 99, 132, 0.2)",
      "rgba(54, 162, 235, 0.2)",
      "rgba(255, 206, 86, 0.2)",
      "rgba(75, 192, 192, 0.2)",
      "rgba(153, 102, 255, 0.2)",
      "rgba(255, 159, 64, 0.2)",
    ];
    const borderColor= [
      "rgba(255, 99, 132, 1)",
      "rgba(54, 162, 235, 1)",
      "rgba(255, 206, 86, 1)",
      "rgba(75, 192, 192, 1)",
      "rgba(153, 102, 255, 1)",
      "rgba(255, 159, 64, 1)",
    ];
  
    data.forEach(myFunction)
  
    function myFunction(item, index, arr) {
      var data_dict={
        'label':labels[index],
        'data':item,
        'backgroundColor':backgroundColor[index],
        'borderColor':borderColor[index]
      };
  
      datasets[index]=data_dict
    }
    
    console.log("datasets", datasets);
  
  
    var monthly_data = {
      labels: months,
      datasets:datasets
    };
    
    var chartOptions = {
      responsive: true,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      stacked: false,
      plugins: {
        title: {
          display: true,
          text: 'Monthly Income Chart'
        }
      }
    };
    

    if(window.lineChart != undefined){
      window.lineChart.destroy();
    }
      window.lineChart = new Chart(speedCanvas, {
      type: 'line',
      data: monthly_data,
      options: chartOptions
    });
  };
  
  const getChartData2 = () => {
    console.log("try fetch");
    fetch("/income/income_category_summary2")
      .then((res) => res.json())
      .then((results) => {
        
        const category_data = results.expense_category_data;
        const [labels, data] = [
          Object.keys(category_data),
          Object.values(category_data),
        ];
        const months=results.months;
      renderChart2(data, labels, months);
      });
  };
  
  document.onload = getChartData();
  document.onload = getChartData2();
