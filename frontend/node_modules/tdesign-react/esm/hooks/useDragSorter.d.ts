interface DragSortProps<T> {
    sortOnDraggable: boolean;
    onDragSort?: (context: DragSortContext<T>) => void;
    onDragOverCheck?: {
        x?: boolean;
        targetClassNameRegExp?: RegExp;
    };
}
type DragFnType = (e?: React.DragEvent<HTMLTableRowElement>, index?: number, record?: any) => void;
interface DragSortInnerData {
    dragging?: boolean;
    draggable?: boolean;
    onDragStart?: DragFnType;
    onDragOver?: DragFnType;
    onDrop?: DragFnType;
    onDragEnd?: DragFnType;
}
export interface DragSortInnerProps extends DragSortInnerData {
    getDragProps?: (index?: number, record?: any) => DragSortInnerData;
}
export interface DragSortContext<T> {
    currentIndex: number;
    current: T;
    targetIndex: number;
    target: T;
}
declare function useDragSorter<T>(props: DragSortProps<T>): DragSortInnerProps;
export default useDragSorter;
