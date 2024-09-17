// Views
import SecretariaView from './components/Views/SecretariaView';
import PessoaView from './components/Views/PessoaView';

const applyConfig = (config) => {
  config.settings = {
    ...config.settings,
    isMultilingual: false,
    supportedLanguages: ['pt-br'],
    defaultLanguage: 'pt-br',
  };
  // Views
  config.views.contentTypesViews = {
    ...config.views.contentTypesViews,
    Secretaria: SecretariaView,
    Pessoa: PessoaView,
  };
  return config;
};

export default applyConfig;
