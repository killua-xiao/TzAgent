import isDate from 'validator/lib/isDate';
import isEmail from 'validator/lib/isEmail';
import isURL from 'validator/lib/isURL';
import { CustomValidator, FormRule, ValueType, AllValidateResult } from './type';
export declare function isValueEmpty(val: ValueType): boolean;
declare const VALIDATE_MAP: {
    date: typeof isDate;
    url: typeof isURL;
    email: typeof isEmail;
    required: (val: ValueType) => boolean;
    whitespace: (val: ValueType) => boolean;
    boolean: (val: ValueType) => boolean;
    max: (val: ValueType, num: number) => boolean;
    min: (val: ValueType, num: number) => boolean;
    len: (val: ValueType, num: number) => boolean;
    number: (val: ValueType) => boolean;
    enum: (val: ValueType, strs: Array<string>) => boolean;
    idcard: (val: ValueType) => boolean;
    telnumber: (val: ValueType) => boolean;
    pattern: (val: ValueType, regexp: RegExp) => boolean;
    validator: (val: ValueType, validate: CustomValidator) => ReturnType<CustomValidator>;
};
export type ValidateFuncType = (typeof VALIDATE_MAP)[keyof typeof VALIDATE_MAP];
/**
 * 校验某一条数据的某一条规则，一种校验规则不满足则不再进行校验。
 * @param value 值
 * @param rule 校验规则
 * @returns 两种校验结果，一种是内置校验规则的校验结果哦，二种是自定义校验规则（validator）的校验结果
 */
export declare function validateOneRule(value: ValueType, rule: FormRule): Promise<AllValidateResult>;
export declare function validate(value: ValueType, rules: Array<FormRule>): Promise<AllValidateResult[]>;
/**
 * Replace with template.
 * `${name} is wrong` + { name: 'password' } = password is wrong
 */
export declare function parseMessage(template: string, options: Record<string, string>): string;
export {};
