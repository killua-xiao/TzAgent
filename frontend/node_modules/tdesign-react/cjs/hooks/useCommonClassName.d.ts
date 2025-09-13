export default function useCommonClassName(): {
    SIZE: {
        default: string;
        xs: string;
        small: string;
        medium: string;
        large: string;
        xl: string;
        block: string;
    };
    STATUS: {
        loading: string;
        disabled: string;
        focused: string;
        success: string;
        error: string;
        warning: string;
        selected: string;
        active: string;
        checked: string;
        current: string;
        hidden: string;
        visible: string;
        expanded: string;
        indeterminate: string;
    };
    sizeClassNames: {
        default: string;
        xs: string;
        small: string;
        medium: string;
        large: string;
        xl: string;
        block: string;
    };
    statusClassNames: {
        loading: string;
        disabled: string;
        focused: string;
        success: string;
        error: string;
        warning: string;
        selected: string;
        active: string;
        checked: string;
        current: string;
        hidden: string;
        visible: string;
        expanded: string;
        indeterminate: string;
    };
    classPrefix: string;
};
export type CommonClassNameType = ReturnType<typeof useCommonClassName>;
