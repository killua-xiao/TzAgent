import { DialogMethod, DialogConfirmMethod, DialogAlertMethod } from './type';
export interface DialogPluginType extends DialogMethod {
    alert: DialogAlertMethod;
    confirm: DialogConfirmMethod;
}
export declare const DialogPlugin: DialogPluginType;
