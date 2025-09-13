import type { TdFormProps, FormValidateResult, FormResetParams, FormValidateMessage, NamePath } from '../type';
export default function useInstance(props: TdFormProps, formRef: any, formMapRef: React.MutableRefObject<Map<any, any>>, floatingFormDataRef: React.RefObject<Record<any, any>>): {
    submit: (e?: React.FormEvent<HTMLFormElement>) => void;
    reset: (params: FormResetParams<FormData>) => void;
    validate: (param?: Record<string, any>) => Promise<FormValidateResult<FormData>>;
    validateOnly: (param?: Record<string, any>) => Promise<FormValidateResult<FormData>>;
    clearValidate: (fields?: Array<keyof FormData>) => void;
    setFields: (fields?: any[]) => void;
    setFieldsValue: (fields?: {}) => void;
    setValidateMessage: (message: FormValidateMessage<FormData>) => void;
    getValidateMessage: (fields?: Array<keyof FormData>) => {};
    getFieldValue: (name: NamePath) => any;
    getFieldsValue: (nameList: string[] | boolean) => {};
    currentElement: any;
    getCurrentElement: () => any;
};
