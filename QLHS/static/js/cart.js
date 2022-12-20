
function timDiem(khoi, lop, mon, hocki, namhoc) {
    fetch('/api/index', {
        method: "post",
        body: JSON.stringify({
               "khoi": khoi,
               "lop": lop,
               "mon": mon,
               "hocki": hocki,
               "namhoc": namhoc,

        }),
        headers: {
            "Content-Type": "application/json"
        }
        }).then(res => res.json()).then(data => {
        console.info(data)
        let d = document.getElementsByClassName("inform")
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity
    })
        }
}
