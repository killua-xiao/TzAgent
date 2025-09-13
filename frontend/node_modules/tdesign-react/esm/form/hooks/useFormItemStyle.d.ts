import React from 'react';
export default function useFormItemStyle(props: any): {
    formItemClass: string;
    formItemLabelClass: string;
    contentClass: () => string;
    labelStyle: {};
    contentStyle: {};
    helpNode: React.JSX.Element;
    extraNode: React.JSX.Element;
};
