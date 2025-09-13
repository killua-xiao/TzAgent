type AnyFunction = (...args: unknown[]) => unknown;
/**
 * Similar to useCallback, with a few subtle differences:
 * - The returned function is a stable reference, and will always be the same between renders
 * - No dependency lists required
 * - Properties or state accessed within the callback will always be "current"
 */
export default function useEventCallback<TCallback extends AnyFunction>(callback: TCallback): TCallback;
export {};
