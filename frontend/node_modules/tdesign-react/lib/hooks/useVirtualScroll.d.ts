/**
 * 通用虚拟滚动，可支持 Select/List/Table/TreeSelect/Cascader 等组件
 */
import { MutableRefObject } from 'react';
import type { ScrollToElementParams, TScroll } from '../common';
export type UseVirtualScrollParams = {
    /** 列数据 */
    data: {
        [key: string]: any;
    }[];
    scroll: TScroll & {
        fixedRows?: Array<number>;
    };
};
declare const useVirtualScroll: (container: MutableRefObject<HTMLElement>, params: UseVirtualScrollParams) => {
    visibleData: any[];
    translateY: number;
    scrollHeight: number;
    isVirtualScroll: boolean;
    handleScroll: () => void;
    handleRowMounted: (rowData: any) => void;
    scrollToElement: (p: ScrollToElementParams) => void;
};
export type VirtualScrollConfig = ReturnType<typeof useVirtualScroll>;
export default useVirtualScroll;
