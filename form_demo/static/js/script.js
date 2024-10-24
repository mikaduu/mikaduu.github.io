const menuContainer=document.querySelector('.menu-container')
const menuIcon = document.getElementById('menu-icon');
const menu = document.getElementById('menu');

// 为菜单图标添加点击事件
menuIcon.addEventListener('click', (event) => {
    //menuIcon.classList.toggle('active');
    if (menu.classList.contains('active')) {
        menu.classList.remove('active');
        menuContainer.classList.remove('active');
        menuIcon.classList.remove('active');
    } else {
        menu.classList.add('active'); 
        menuContainer.classList.add('active');
        menuIcon.classList.add('active');
    }
    // 阻止事件冒泡
    event.stopPropagation();
});

// 点击空白处隐藏菜单
document.addEventListener('click', (event) => {
    if (!menu.contains(event.target) && event.target !== menuIcon) {
        //menuIcon.classList.toggle('active');
        //menuContainer.classList.toggle('active');
        if (menu.classList.contains('active')) {
            menu.classList.remove('active');
            menuContainer.classList.remove('active');
            menuIcon.classList.remove('active');
        } 
    }
});
