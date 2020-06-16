const navSlide = () => {
	const burger = document.querySelector(".burger");
	const nav = document.querySelector(".nav-links");
	const navLinks = document.querySelectorAll(".nav-links li");
	
	burger.addEventListener('click',() => {
		// Toggle Nav
		nav.classList.toggle('nav-active');
	
		//Animate Links
		navLinks.forEach((link, index) => {
			if(link.style.animation){
				link.style.animation = '';
			} else {
				link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 0.7}s`;
			}
		});
		//Burger Animation
		burger.classList.toggle("toggle");
	});
	
	
}

const tabSlide = () => {
	const container = document.querySelector(".tab");
	const burger = container.querySelector(".burger");
	console.log(burger);
	const tab = container.querySelector(".tab-nav");
	const tabLinks = container.querySelectorAll(".tab-nav li");
	
	burger.addEventListener('click',() => {
		// Toggle Nav
		tab.classList.toggle('tab-active');
	
		//Burger Animation
		burger.classList.toggle("toggle");
	});
	
	
}

const tabShow = () => {
	var li_elements = document.querySelectorAll(".tab ul li");
	
	var item_elements = document.querySelectorAll(".item");
	for (var i = 0; i < li_elements.length; i++) {
		li_elements[i].addEventListener("click", function() {
			li_elements.forEach(function(li) {
			  li.classList.remove("active");
			});
			this.classList.add("active");
			var li_value = this.getAttribute("data-li");
			item_elements.forEach(function(item) {
			  item.style.display = "none";
			});
			if (li_value == "all") {
			  document.querySelector("." + li_value).style.display = "block";
			} else if (li_value == "fresh") {
			  document.querySelector("." + li_value).style.display = "block";
			} else if (li_value == "grains") {
			  document.querySelector("." + li_value).style.display = "block";
			} else if (li_value == "baking") {
			  document.querySelector("." + li_value).style.display = "block";
			} else if (li_value == "canned") {
			  document.querySelector("." + li_value).style.display = "block";
			} else if (li_value == "drinks") {
			  document.querySelector("." + li_value).style.display = "block";
			} else if (li_value == "snacks") {
			  document.querySelector("." + li_value).style.display = "block";
			} else if (li_value == "other") {
			  document.querySelector("." + li_value).style.display = "block";
		    } else if (li_value == "ingredients") {
			  document.querySelector("." + li_value).style.display = "block";
		    } else if (li_value == "method") {
			  document.querySelector("." + li_value).style.display = "block";
			} else {
			  console.log("");
			}
		  });
	}
}

	
const makeCarousel = (carousel_item) => {
	const track = carousel_item.querySelector('.carousel__track');
	const slides = Array.from(track.children);
	const img = carousel_item.querySelectorAll('.carousel__images');
	console.log(img)
	const nextButton = carousel_item.querySelector('.carousel__button--right');
	const prevButton = carousel_item.querySelector('.carousel__button--left');
	const dotsNav = carousel_item.querySelector('.carousel__nav');
	const dots = Array.from(dotsNav.children);

	const slideWidth = img[0].getBoundingClientRect().width;


	const setSlidePosition = (slide, index) => {
		slide.style.left = slideWidth * index + 'px';
	}

	const moveToSlide = (track, currentSlide, targetSlide) => {
		track.style.transform = 'translateX(-' + targetSlide.style.left + ')';
		currentSlide.classList.remove('current-slide');
		targetSlide.classList.add('current-slide');
		
	}

	const updateDots = (currentDot,targetDot) => {
		currentDot.classList.remove('current-slide');
		targetDot.classList.add('current-slide');
	}

	const updateArrows = (targetIndex) => {
		
		if (targetIndex === 0) {
			prevButton.classList.add('is-hidden');
			nextButton.classList.remove('is-hidden');
		} else if (targetIndex === slides.length - 3) {
			prevButton.classList.remove('is-hidden');
			nextButton.classList.add('is-hidden');
		} else {
			prevButton.classList.remove('is-hidden');
			nextButton.classList.remove('is-hidden');
		}
	}

	slides.forEach(setSlidePosition);

	// when I click left, move slides to the left
	prevButton.addEventListener('click', e => {
		const currentSlide = track.querySelector('.current-slide');
		const prevSlide = currentSlide.previousElementSibling;
		const currentDot = dotsNav.querySelector('.current-slide');
		const prevDot = currentDot.previousElementSibling;
		const prevIndex = dots.findIndex(dot => dot === prevDot);
		
		moveToSlide(track, currentSlide, prevSlide);
		updateDots(currentDot,prevDot);
		updateArrows(prevIndex);
	})


	// when I click right, move slides to the right
	nextButton.addEventListener('click', e => {
		const currentSlide = track.querySelector('.current-slide');
		const nextSlide = currentSlide.nextElementSibling;
		const currentDot = dotsNav.querySelector('.current-slide');
		const nextDot = currentDot.nextElementSibling;
		const nextIndex = dots.findIndex(dot => dot === nextDot);
		
		moveToSlide(track, currentSlide, nextSlide);
		updateDots(currentDot,nextDot);
		updateArrows(nextIndex);
	})

	// when I click the nav indicators, move to the slide
	dotsNav.addEventListener('click', e => {
		// what indicator was clicked on?
		const targetDot = e.target.closest('button');
		
		if (!targetDot) return;
		
		const currentSlide = track.querySelector('.current-slide');
		const currentDot = dotsNav.querySelector('.current-slide');
		const targetIndex = dots.findIndex(dot => dot === targetDot);
		const targetSlide = slides[targetIndex];
		
		moveToSlide(track, currentSlide, targetSlide);
		updateDots(currentDot,targetDot);
		
		updateArrows(targetIndex);
		
	})
}

const carouselAnimate = () => {
	
	const carousel = document.querySelectorAll('.carousel');

	for (var i = 0; i < carousel.length; i++) { 

		makeCarousel(carousel[i]);
	}
}
	

const app = () => {
	navSlide();
	tabShow();
	carouselAnimate();
	tabSlide();
}

app()