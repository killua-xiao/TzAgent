export default function useMutationObservable(targetEl: HTMLElement | null, cb: MutationCallback, options?: {
    debounceTime: number;
    config: MutationObserverInit;
}): void;
