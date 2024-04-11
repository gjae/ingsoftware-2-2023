window.onload = () => {
    /**
     * Este evento hace que el panel lateral para los pagos, en caso de estar en
     * una vista que no sea una pantalla de telefono
     * baje cuando se hace scroll de modo que el usuario siempre vera la caja con el boton
     * de hacer el donativo
     */
    window.addEventListener("scroll", (e)=> {
        if (window.scrollY > 1) {
            console.log("STICKY")
            document.getElementById("sticky-area").classList.add("sticky-area")
        } else {
            document.getElementById("sticky-area").classList.remove("sticky-area")
        }
    })

}
