// Blocos
/// Gestor
import GestorEdit from './components/Blocks/GestorBlock/Edit';
import GestorView from './components/Blocks/GestorBlock/View';
import gestorSVG from '@plone/volto/icons/user.svg';

// Views
import SecretariaView from './components/Views/SecretariaView';
import PessoaView from './components/Views/PessoaView';

const applyConfig = (config) => {
  config.settings = {
    ...config.settings,
    isMultilingual: false,
    supportedLanguages: ['pt-br'],
    defaultLanguage: 'pt-br',
    contextualVocabularies: ['portal.governo.vocabulary.gestores'],
  };
  // Views
  config.views.contentTypesViews = {
    ...config.views.contentTypesViews,
    Secretaria: SecretariaView,
    Pessoa: PessoaView,
  };

  // Blocos
  /// Grupos de Blocos
  config.blocks.groupBlocksOrder = [
    ...config.blocks.groupBlocksOrder,
    { id: 'procergs', title: 'Procergs' },
  ];
  /// Bloco Gestor
  config.blocks.blocksConfig.gestorBlock = {
    id: 'gestorBlock',
    title: 'Gestor',
    group: 'procergs',
    icon: gestorSVG,
    edit: GestorEdit,
    view: GestorView,
    sidebar: 1,
  };

  return config;
};

export default applyConfig;
