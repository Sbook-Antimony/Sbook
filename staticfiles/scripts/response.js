setInterval(function() {
    for(let element of  jQuery("[hover-class]")) {
        let classes = element.getAttribute("hover-class");
        if(!classes || classes == "false") continue;
        element.setAttribute("hover-class", false);

        cls = classes.split(" ");
        if(cls[0].endsWith(":")) {
            [margin, ...cls] = cls;
            margin = margin.slice(0,-1);
        }
        let ncls = cls.filter((c) => c.startsWith("!"));
        cls = cls.filter((c) => !c.startsWith("!"));
        for(var i = 0; i < ncls.length; i++) ncls[i] = ncls[i].slice(1);
        element.addEventListener("mouseenter", function() {
            try {
                element.classList.add(
                    ...cls
                );
                element.classList.remove(
                    ...ncls
                );
            } catch (e) {

            }
        });
        element.addEventListener("mouseleave", function() {
            try {
                element.classList.add(
                    ...ncls
                );
                element.classList.remove(
                    ...cls
                );
            } catch (e) {

            }
        });
    };
}, 1000);

for(let element of  jQuery("[css-transition]")) {
    element.style.transition = element.getAttribute("css-transition");
};
setInterval(function() {
    for(let element of jQuery("[view-class]")) {
        let margin = "10";
        let classes = element.getAttribute("view-class");
        if(!classes) continue;
        element.setAttribute("view-class", false);
        (new IntersectionObserver(
            (entries, observer) => {
                entries.forEach((entry) => {
                    // Each entry describes an intersection change for one observed
                    // target element:
                    //   entry.boundingClientRect
                    //   entry.intersectionRatio
                    //   entry.intersectionRect
                    //   entry.isIntersecting
                    //   entry.rootBounds
                    //   entry.target
                    //   entry.time


                    cls = classes.split(" ");
                    if(cls[0].endsWith(":")) {
                        [margin, ...cls] = cls;
                        margin = margin.slice(0,-1);
                    }
                    let ncls = cls.filter((c) => c.startsWith("!"));
                    cls = cls.filter((c) => !c.startsWith("!"));
                    for(var i = 0; i < ncls.length; i++) ncls[i] = ncls[i].slice(1);


                    try {
                        if(entry.isIntersecting) {
                            //console.log("added", ...element.getAttribute("view-class").split(" "));
                            element.classList.add(
                                ...cls
                            );
                            element.classList.remove(
                                ...ncls
                            );
                        } else {
                            //console.log("removed", ...element.getAttribute("view-class").split(" "));
                            element.classList.remove(
                                ...cls
                            );
                            element.classList.add(
                                ...ncls
                            );
                        }
                    } catch (e) {

                    }

                });
            },
            {
                root: null,
                rootMargin: margin+"px",
                threshold: [1.0, 0.0],
            },
        )).observe(element);
    };
}, 1000);



function markdown(text) {
    
}


window.addEventListener('scroll', function() {
    let headerBg = jQuery("#header-back-blurred-div");
    if(headerBg.length > 0) {
        headerBg[0].style.backgroundPositionY = (-(window.pageYOffset).toFixed(0)).toString()+"px";
        let t = window.pageYOffset/150;
        if(t > 1) t = 1;
        headerBg[0].style.opacity = (t*t*t).toFixed(2).toString()
        let elts = jQuery("[onviewbg]")
        for(let i = elts.length - 1; i >= 0; i--) {
            let element = elts[i];
            if(window.pageYOffset >= element.offsetTop + 350) {
                element.parentElement.style.transition = "1s",
                element.parentElement.style.backgroundColor = element.getAttribute('onviewbg');
                break;
            }
        };
    }
});
