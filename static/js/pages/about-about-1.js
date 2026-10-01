document.addEventListener("DOMContentLoaded", function(){
    
        const slider = document.getElementById("btrlxSlider");
        const leftBtn = document.getElementById("leftBtn");
        const rightBtn = document.getElementById("rightBtn");
    
        if (!slider) return;
    
        rightBtn.addEventListener("click", function () {
    
            slider.scrollBy({
                left: 380,
                behavior: "smooth"
            });
    
        });
    
        leftBtn.addEventListener("click", function () {
    
            slider.scrollBy({
                left: -380,
                behavior: "smooth"
            });
    
        });
    
    });
