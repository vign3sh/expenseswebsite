function make_dashboard(){

  var exp=[document.getElementById("today_exp"), document.getElementById("week_exp"),
            document.getElementById("month_exp"), document.getElementById("year_exp")]

  var c=[document.getElementById("today_count"),document.getElementById("week_count"),
            document.getElementById("month_count"),document.getElementById("year_count")]

  fetch("/expense_summary")
    .then((res) => res.json())
    .then((results) => {
      console.log("results", results);
      const amount = results.amount;
      const count=results.count

      exp[0].innerHTML+=amount[0];
      exp[1].innerHTML=amount[1];
      exp[2].innerHTML=amount[2];
      exp[3].innerHTML=amount[3];

      c[0].innerHTML=count[0];   
      c[1].innerHTML=count[1];   
      c[2].innerHTML=count[2];
      c[3].innerHTML=count[3];


    });
}

document.onload = make_dashboard()