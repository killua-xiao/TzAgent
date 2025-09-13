/**
 * 管理 object 类型 state 的 Hooks，用法与 class 组件的 this.setState 基本一致。
 * @param initialState
 * @returns [state, setMergeState]
 */
declare const useSetState: <T extends object>(initialState?: T) => [T, (patch: Partial<T> | ((prevState: T) => Partial<T>)) => void];
export default useSetState;
