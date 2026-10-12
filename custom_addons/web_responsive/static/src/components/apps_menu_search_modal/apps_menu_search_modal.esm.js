/* global document, location, window */

import {Component, useState, useRef, onMounted} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";
import {debounce} from "@web/core/utils/timing";
import {fuzzyLookup} from "@web/core/utils/search";
import {browser} from "@web/core/browser/browser";
import {
    updateMenuWebIconData,
    updateMenuDisplayName,
} from "@web_responsive/components/apps_menu_tools.esm";

export class AppsMenuSearchModal extends Component {
    setup() {
        super.setup();
        this.state = useState({
            hasQuery: false,
            apps: [],
            menuItems: [],
            selectedIndex: 0,
        });
        this.searchInputRef = useRef("searchInput");
        this.menuService = useService("menu");
        this.rootMenuItems = this._getRootMenuItems();
        this.subMenuItems = this._getSubMenuItems();
        this._searchMenus = debounce(this._searchMenus.bind(this), 150);

        onMounted(() => {
            if (this.searchInputRef.el) {
                this.searchInputRef.el.focus();
            }
        });
    }

    _getRootMenuItems() {
        return this.menuService.getApps().reduce((memo, menu) => {
            if (menu.actionID && menu.appID === menu.id) {
                const menuCopy = Object.assign({}, menu);
                updateMenuWebIconData(menuCopy);
                updateMenuDisplayName(menuCopy);
                if (menuCopy.actionPath) {
                    menuCopy.path = `/odoo/${menuCopy.actionPath}`;
                } else {
                    menuCopy.path = `/odoo/action-${menuCopy.actionID}`;
                }
                memo.push(menuCopy);
            }
            return memo;
        }, []);
    }

    _getSubMenuItems() {
        const response = [];
        for (const menu of this.menuService.getApps()) {
            const menuTree = this.menuService.getMenuAsTree(menu.id);
            this._collectSubMenuItems(response, null, menuTree);
        }
        return response;
    }

    _collectSubMenuItems(memo, parentMenu, menu) {
        const menuCopy = Object.assign({}, menu);
        updateMenuDisplayName(menuCopy);
        if (parentMenu) {
            menuCopy.displayName = `${parentMenu.displayName} / ${menuCopy.displayName}`;
        }
        if (menuCopy.actionID && !(menuCopy.actionID && menuCopy.appID === menuCopy.id)) {
            for (const root of this.rootMenuItems) {
                if (menuCopy.appID === root.appID) {
                    if (root.actionPath) {
                        menuCopy.path = `/odoo/${root.actionPath}/action-${menuCopy.actionID}`;
                    } else {
                        menuCopy.path = `/odoo/action-${menuCopy.actionID}`;
                    }
                    break;
                }
            }
            memo.push(menuCopy);
        }
        for (const child of menuCopy.childrenTree || []) {
            this._collectSubMenuItems(memo, menuCopy, child);
        }
        return memo;
    }

    onSearchInput() {
        const query = this.inputValue;
        this.state.hasQuery = query.length > 0;
        if (this.state.hasQuery) {
            this._searchMenus(query);
        } else {
            this.state.apps = [];
            this.state.menuItems = [];
        }
        this.state.selectedIndex = 0;
    }

    _searchMenus(query) {
        const searchField = (item) => item.displayName;
        this.state.apps = fuzzyLookup(query, this.rootMenuItems, searchField);
        this.state.menuItems = fuzzyLookup(query, this.subMenuItems, searchField);
    }

    get inputValue() {
        const {el} = this.searchInputRef;
        return el ? el.value.trim() : "";
    }

    get totalItems() {
        return this.state.apps.length + this.state.menuItems.length;
    }

    getItemClass(index, type) {
        const classes = ["o_app_search_modal__item"];
        if (type === "app") {
            classes.push("o_app_search_modal__item--app");
        }
        if (index === this.state.selectedIndex) {
            classes.push("o_app_search_modal__item--focused");
        }
        return classes.join(" ");
    }

    onItemMouseEnter(ev) {
        const index = parseInt(ev.currentTarget.dataset.index, 10);
        if (!isNaN(index)) {
            this.state.selectedIndex = index;
        }
    }

    onItemClick(ev) {
        const index = parseInt(ev.currentTarget.dataset.index, 10);
        if (isNaN(index)) return;

        const {apps, menuItems} = this.state;
        if (index < apps.length) {
            this._selectApp(apps[index], ev);
        } else {
            const menuIndex = index - apps.length;
            if (menuIndex < menuItems.length) {
                this._selectMenu(menuItems[menuIndex], ev);
            }
        }
    }

    onKeyDown(ev) {
        const code = ev.code;

        if (code === "Escape") {
            ev.preventDefault();
            ev.stopPropagation();
            this.props.onClose();
        } else if (code === "ArrowDown") {
            ev.preventDefault();
            if (this.totalItems > 0) {
                this.state.selectedIndex = (this.state.selectedIndex + 1) % this.totalItems;
                this._scrollToSelected();
            }
        } else if (code === "ArrowUp") {
            ev.preventDefault();
            if (this.totalItems > 0) {
                this.state.selectedIndex = (this.state.selectedIndex - 1 + this.totalItems) % this.totalItems;
                this._scrollToSelected();
            }
        } else if (code === "Enter") {
            ev.preventDefault();
            const {apps, menuItems, selectedIndex} = this.state;
            if (selectedIndex < apps.length) {
                this._selectApp(apps[selectedIndex], ev);
            } else {
                const menuIndex = selectedIndex - apps.length;
                if (menuIndex < menuItems.length) {
                    this._selectMenu(menuItems[menuIndex], ev);
                }
            }
        } else if (code === "Tab") {
            ev.preventDefault();
            if (this.totalItems > 0) {
                if (ev.shiftKey) {
                    this.state.selectedIndex = (this.state.selectedIndex - 1 + this.totalItems) % this.totalItems;
                } else {
                    this.state.selectedIndex = (this.state.selectedIndex + 1) % this.totalItems;
                }
                this._scrollToSelected();
            }
        } else if (code === "Home") {
            this.state.selectedIndex = 0;
            this._scrollToSelected();
        } else if (code === "End") {
            this.state.selectedIndex = Math.max(0, this.totalItems - 1);
            this._scrollToSelected();
        }
    }

    _scrollToSelected() {
        setTimeout(() => {
            const el = document.querySelector(".o_app_search_modal__item--focused");
            if (el) {
                el.scrollIntoView({block: "nearest", behavior: "smooth"});
            }
        }, 0);
    }

    _selectApp(app, ev) {
        const openInNewTab = ev && (ev.ctrlKey || ev.metaKey);
        if (openInNewTab && app.path) {
            browser.open(app.path, "_blank");
        } else {
            this.menuService.selectMenu(app);
        }
        this.props.onClose();
    }

    _selectMenu(menu, ev) {
        const openInNewTab = ev && (ev.ctrlKey || ev.metaKey);
        if (openInNewTab && menu.path) {
            browser.open(menu.path, "_blank");
        } else {
            this.menuService.selectMenu(menu);
        }
        this.props.onClose();
    }

    onBackdropClick(ev) {
        this.props.onClose();
    }
}

AppsMenuSearchModal.props = {
    onClose: Function,
};
AppsMenuSearchModal.template = "web_responsive.AppsMenuSearchModal";
