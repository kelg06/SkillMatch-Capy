console.log("JS is working!");


// Sidebar
const menuItems = document.querySelectorAll('.menu-item');

// Theme
const theme = document.querySelector('#theme');
const themeModal = document.querySelector('.customize-theme');
const fontSize = document.querySelectorAll('.choose-size span');
var root = document.querySelector(':root');
const colorPalette = document.querySelectorAll('.choose-color span');
const Bg1 = document.querySelector('.bg-1');
const Bg2 = document.querySelector('.bg-2');
const Bg3 = document.querySelector('.bg-3');

// Popup
document.addEventListener("DOMContentLoaded", function() {
    const dialog = document.getElementById("profile");

    window.show_modal = function() {
        dialog.showModal();
    };

    // Close the dialog when clicking outside the content
    dialog.addEventListener("click", function(event) {
        const rect = dialog.getBoundingClientRect();
        const clickedInDialog = (
            event.clientX >= rect.left &&
            event.clientX <= rect.right &&
            event.clientY >= rect.top &&
            event.clientY <= rect.bottom
        );

        if (!clickedInDialog) {
            dialog.close();
        }
    });
});

// ============== SIDEBAR ============== 

// Remove active class from all menu items
const changeActiveItem = () => {
    menuItems.forEach(item => {
        item.classList.remove('active');
    })
}

menuItems.forEach(item => {
    item.addEventListener('click', () => {
        changeActiveItem();
        item.classList.add('active');
    })
})

// ============== THEME / DISPLAY CUSTOMIZATION ============== 

// Opens Modal
const openThemeModal = () => {
    themeModal.style.display = 'grid';
}

// Closes Modal
const closeThemeModal = (e) => {
    if(e.target.classList.contains('customize-theme')) {
        themeModal.style.display = 'none';
    }
}

themeModal.addEventListener('click', closeThemeModal);
theme.addEventListener('click', openThemeModal);

// ============== FONT SIZE ============== 

// remove active class from spans or font size selectors
const removeSizeSelectors = () => {
    fontSize.forEach(size => {
        size.classList.remove('active');
    })
}

fontSize.forEach(size => { 
   size.addEventListener('click', () => {
        removeSizeSelectors();
        let fontSize;
        size.classList.toggle('active');

        if(size.classList.contains('font-size-1')) { 
            fontSize = '10px';
        } else if(size.classList.contains('font-size-2')) { 
            fontSize = '13px';
        } else if(size.classList.contains('font-size-3')) {
            fontSize = '16px';
        } else if(size.classList.contains('font-size-4')) {
            fontSize = '19px';
        } else if(size.classList.contains('font-size-5')) {
            fontSize = '22px';
        }

        // change font size of the root html element
        document.querySelector('html').style.fontSize = fontSize;
   })
})

// Remove active class from colors
const changeActiveColorClass = () => {
    colorPalette.forEach(colorPicker => {
        colorPicker.classList.remove('active');
    })
}

// Change color primary
colorPalette.forEach(color => {
    color.addEventListener('click', () => {
        let primaryHue;
        changeActiveColorClass(); 

        if(color.classList.contains('color-1')) {
            primaryHue = 252;
        } else if(color.classList.contains('color-2')) {
            primaryHue = 52;
        } else if(color.classList.contains('color-3')) {
            primaryHue = 352;
        } else if(color.classList.contains('color-4')) {
            primaryHue = 152;
        } else if(color.classList.contains('color-5')) {
            primaryHue = 202;
        }

        color.classList.add('active');
        root.style.setProperty('--primary-color-hue', primaryHue);
    })
})

// Theme Background Values
let lightColorLightness;
let whiteColorLightness;
let darkColorLightness;

// Changes background color
const changeBG = () => {
    root.style.setProperty('--light-color-lightness', lightColorLightness);
    root.style.setProperty('--white-color-lightness', whiteColorLightness);
    root.style.setProperty('--dark-color-lightness', darkColorLightness);
}

Bg1.addEventListener('click', () => {
    // add active class
    Bg1.classList.add('active');
    // remove active class from the others
    Bg2.classList.remove('active');
    Bg3.classList.remove('active');
    //remove customized changes from local storage
    window.location.reload();
});

Bg2.addEventListener('click', () => {
    darkColorLightness = '95%';
    whiteColorLightness = '20%';
    lightColorLightness = '15%';

    // add active class
    Bg2.classList.add('active');
    // remove active class from the others
    Bg1.classList.remove('active');
    Bg3.classList.remove('active');
    changeBG();
});

Bg3.addEventListener('click', () => {
    darkColorLightness = '95%';
    whiteColorLightness = '10%';
    lightColorLightness = '0%';

    // add active class
    Bg3.classList.add('active');
    // remove active class from the others
    Bg1.classList.remove('active');
    Bg2.classList.remove('active');
    changeBG();
});