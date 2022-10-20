function make_dashboard(){

  var exp=[document.getElementById("today_exp"), document.getElementById("week_exp"),
            document.getElementById("month_exp"), document.getElementById("year_exp")]

  var count=[document.getElementById("today_count"),document.getElementById("week_count"),
            document.getElementById("month_count"),document.getElementById("year_count")]

  fetch("/expense_summary")
    .then((res) => res.json())
    .then((results) => {
      console.log("results", results);
      const amount = results.amount;
      const count=results.count

      exp[0].innerHTML=amount[0]
      exp[1].innerHTML=amount[1]
    });
}

document.onload = make_dashboard()