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


const getChartData = () => {

  fetch("/expense_summary")
    .then((res) => res.json())
    .then((results) => {
      
      const category_data = results.expense_category_data;
      const [labels, data] = [
        Object.keys(category_data),
        Object.values(category_data),
      ];
      const months=results.months;
    renderChart(data, labels, months);
    });
};
document.onload = make_dashboard()
document.onload = getChartData()
