/* Copyright 2018 Tecnativa - Jairo Llopis
 * Copyright 2021 ITerra - Sergey Shebanin
 * Copyright 2023 Onestein - Anjeel Haria
 * Copyright 2023 Taras Shabaranskyi
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */

export function getWebIconData(menu) {
    // If webIconData is already available, use it directly
    if (menu.webIconData) {
        const iconData = menu.webIconData;
        if (iconData.startsWith("data:image")) {
            return iconData;
        }
        const prefix = iconData.startsWith("P")
            ? "data:image/svg+xml;base64,"
            : "data:image/png;base64,";
        return prefix + iconData.replace(/\s/g, "");
    }
    // If webIcon has exactly 2 parts (module,path format), treat as file path
    const webIcon = menu.webIcon;
    if (webIcon && webIcon.split(",").length === 2) {
        const path = webIcon.replace(",", "/");
        return path.startsWith("/") ? path : "/" + path;
    }
    // Default fallback icon
    return "/web_responsive/static/img/default_icon_app.png";
}

/**
 * Parse webIcon string into an object if it has 3 parts
 * @param {Object} menu
 * @returns {Object|null} {iconClass, color, backgroundColor} or null
 */
export function getWebIconObject(menu) {
    const webIcon = menu.webIcon;
    if (!webIcon) {
        return null;
    }
    const parts = webIcon.split(",");
    if (parts.length === 3) {
        const [iconClass, color, backgroundColor] = parts;
        return { iconClass, color, backgroundColor };
    }
    return null;
}

/**
 * @param {Object} menu
 */
export function updateMenuWebIconData(menu) {
    menu.webIconData = menu.webIconData ? getWebIconData(menu) : "";
    menu.webIconObject = getWebIconObject(menu);
}

export function updateMenuDisplayName(menu) {
    menu.displayName = menu.name.trim();
}

/**
 * @param {Object} menu
 * @returns {Boolean}
 */
export function isRootMenu(menu) {
    return menu.actionID && menu.appID === menu.id;
}

/**
 * @param {Object[]} memo
 * @param {Object|null} parentMenu
 * @param {Object} menu
 * @returns {Object[]}
 */
export function collectSubMenuItems(memo, parentMenu, menu) {
    const menuCopy = Object.assign({}, menu);
    updateMenuDisplayName(menuCopy);
    if (parentMenu) {
        menuCopy.displayName = `${parentMenu.displayName} / ${menuCopy.displayName}`;
    }
    if (menuCopy.actionID && !isRootMenu(menuCopy)) {
        memo.push(menuCopy);
    }
    for (const child of menuCopy.childrenTree || []) {
        collectSubMenuItems(memo, menuCopy, child);
    }
    return memo;
}

/**
 * @param {Object[]} memo
 * @param {Object} menu
 * @returns {Object}
 */
export function collectRootMenuItems(memo, menu) {
    if (isRootMenu(menu)) {
        const menuCopy = Object.assign({}, menu);
        updateMenuWebIconData(menuCopy);
        updateMenuDisplayName(menuCopy);
        memo.push(menuCopy);
    }
    return memo;
}
