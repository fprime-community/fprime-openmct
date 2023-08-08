export namespace MENU_PLACEMENT {
    let TOP: string;
    let TOP_LEFT: string;
    let TOP_RIGHT: string;
    let BOTTOM: string;
    let BOTTOM_LEFT: string;
    let BOTTOM_RIGHT: string;
    let LEFT: string;
    let RIGHT: string;
}
export default Menu;
declare class Menu {
    constructor(options: any);
    options: any;
    dismiss(): void;
    show(): void;
    showMenu(): void;
    showSuperMenu(): void;
    component: import("vue/types/vue").CombinedVueInstance<Vue, object, object, object, Record<never, any>> | undefined;
    /**
     * @private
     */
    private _calculatePopupPosition;
    /**
     * @private
     */
    private _getMenuPositionBasedOnPlacement;
    /**
     * @private
     */
    private _preventMenuOverflow;
}
import Vue from 'vue';
//# sourceMappingURL=menu.d.ts.map