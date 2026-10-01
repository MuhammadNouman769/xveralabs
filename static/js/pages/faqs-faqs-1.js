document.querySelectorAll(".faq-item").forEach(item => {

    item.addEventListener("click", () => {

        document.querySelectorAll(".faq-item").forEach(el => {

            if(el !== item){
                el.classList.remove("active");
            }

        });

        item.classList.toggle("active");

    });

});
