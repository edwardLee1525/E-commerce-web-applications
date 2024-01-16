const sale_price = document.querySelectorAll('.bd i');
const normal_price = document.querySelectorAll('.bd span');
for (let i = 0; i < sale_price.length; i++) {
    if (sale_price[i].textContent !== 'None') {
        sale_price[i].style.marginRight = "6px";
        normal_price[i].style.textDecoration = "line-through";
        normal_price[i].style.fontSize = "17px";
        normal_price[i].style.color = "#c2baba";
    } else {
        sale_price[i].innerHTML = '';
    }
}