    const wineprice = document.querySelector('.wineprice');
    const winepricelabel = document.querySelector(".wineprice-label")

    function headleinput() {
        console.log(wineprice.value)
        if (winepricelabel.textContent) {
            winepricelabel.textContent = "";
            winepricelabel.textContent = wineprice.value * 10000 + " 원"
            if (winepricelabel.textContent == "200000 원") {
                winepricelabel.textContent = "전체 가격"
            }
            wineprice.setAttribute("value", wineprice.value)
        }
    }

    wineprice.addEventListener('input', headleinput)