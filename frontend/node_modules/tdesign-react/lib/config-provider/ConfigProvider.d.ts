import React from 'react';
import { Config } from './ConfigContext';
import { GlobalConfigProvider } from './type';
export interface ConfigProviderProps extends Config {
    children: React.ReactNode;
    /**
     * 不需要设置全局上下文信息
     * 不传或者false：表示全局上下文变动，需要更新全局上下文的信息放入到变量中
     * true：表示全局上下文信息不需要重新设置，
     * 解决问题：当plugin调用的时候，单独包裹的Provider 也会传全局变量，仅自身可用，多次调用时相互之间不会冲突。
     * 插件单独的config方法依然可用。自身属性通过props传递
     * 例如：多处调用message.config 如果每次都更新全局上下文，插件调用时配置会相互影响，导致行为结果跟预期不一致。
     */
    notSet?: boolean;
}
export declare const merge: (src: GlobalConfigProvider, config: GlobalConfigProvider) => GlobalConfigProvider;
export declare const getGlobalConfig: (configInfo?: GlobalConfigProvider) => GlobalConfigProvider;
export declare const setGlobalConfig: (configInfo?: GlobalConfigProvider) => void;
declare function ConfigProvider({ children, globalConfig, notSet }: ConfigProviderProps): React.JSX.Element;
declare namespace ConfigProvider {
    var getGlobalConfig: (configInfo?: GlobalConfigProvider) => GlobalConfigProvider;
    var setGlobalConfig: (configInfo?: GlobalConfigProvider) => void;
    var displayName: string;
}
export default ConfigProvider;
